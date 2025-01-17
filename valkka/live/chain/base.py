"""
NAME.py :

Copyright 2018 Sampsa Riikonen

Authors: Sampsa Riikonen

This file is part of the Valkka Live video surveillance program

Valkka Live is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/> 

@file    NAME.py
@author  Sampsa Riikonen
@date    2018
@version 1.0.1 
@brief   
"""
import sys
import time
import copy
from enum import Enum

# so, everything that has .core, refers to the api1 level (i.e. swig
# wrapped cpp code)
from valkka import core
# api2 versions of the thread classes
from valkka.api2.threads import LiveThread, USBDeviceThread, OpenGLThread
from valkka.api2.valkkafs import ValkkaFSManager, ValkkaFS
from valkka.api2.tools import parameterInitCheck, typeCheck, generateGetters
from valkka.api2.chains.port import ViewPort


class BaseFilterchain:
    """Common methods to all Filterchains 
    """
    

    def __init__(self, **kwargs):
        pass
    

    def __del__(self):
        self.requestClose()
        
        
    def initVars(self):
        """Assure you have these variables at least
        """
        # client counters
        self.decoding_client_count = 0
        self.x_screen_count = {}
        for i in range(len(self.openglthreads)): 
            self.x_screen_count[i] = 0
        # view port related
        self.ports = []
        self.tokens_by_port = {}


    def decoding_client(self, inc = 0):
        """Count instances that need decoding
        
        Start decoding if the number goes from 0 => 1
        Stop decoding if the number goes from 1 => 0
        """
        pass


    def x_screen_client(self, index, inc = 0):
        """Count instances that require OpenGLThread
        """
        pass


    # *** Sending video to OpenGLThreads ***
            
    def addViewPort(self, view_port: ViewPort):
        """view_port carries information about window id & x-screen
        
        When drag'n'drop happens, the receiving window obtains bytes that a deserialized, typically to device.RTSPCameraDevice = self.device
        
        Then the receiving window searches for the correct filterchain, from a group of filterchains, _id:
        
        ::
        
            fc = filterchain_group.get(_id = self.device._id)
            
        Then this method is called
        
        There should be two filterchain groups: one for live & other one for recorded
        
        For recorder view, when the RootContainer is created, it's passed a different filterchain_group
        
        filterchain_group_live
        filterchain_group_rec
        
        Ideally:
        
        - Drag'n'drop camera to a "recorder container"
        - When "update" is pressed, update filterchains in filterchain_group_live & connect to ValkkaFS (by calling self.setRecording)
        - ..create filterchain into filterchain_group_rec
        
        - For the moment, just have a single recorder (not implemented as a container).  All streams are automatically added to that recorder
        - When recreating / updating filterchain_group_live, do the same for filterchain_group_rec
        
        Live View
        Recording View
            => 1x1 timebar, 2x2 timebar, etc.
            => 1x1, 2x2
        There can only be a single timebar view visible at a moment
            
        """
        
        assert(issubclass(view_port.__class__, ViewPort))
        # ViewPort object is created by the widget .. and stays alive while the
        # widget exists.
        window_id = view_port.getWindowId()
        x_screen_num = view_port.getXScreenNum()
        openglthread = self.openglthreads[x_screen_num]

        if (self.verbose):
            print(self.pre,
                "addViewPort: view_port, window_id, x_screen_num",
                view_port,
                window_id,
                x_screen_num)
        if (view_port in self.ports):
            self.delViewPort(view_port)

        self.x_screen_client(x_screen_num, inc = 1)
        
        # send frames from this slot to correct openglthread and window_id
        print(self.pre, "connecting slot, window_id", self.slot, window_id)
        token = openglthread.connect(slot = self.slot, window_id = window_id)
        print(self.pre, "==> connected slot, window_id, token", self.slot, window_id, token)
        self.tokens_by_port[view_port] = token
        self.ports.append(view_port)


    def delViewPort(self, view_port):
        assert(issubclass(view_port.__class__, ViewPort))
        window_id = view_port.getWindowId()
        x_screen_num = view_port.getXScreenNum()
        openglthread = self.openglthreads[x_screen_num]

        if (self.verbose):
            print(self.pre,
                "delViewPort: view_port, window_id, x_screen_num",
                view_port,
                window_id,
                x_screen_num)
        if (view_port not in self.ports):
            print(self.pre, "delViewPort : FATAL : no such port", view_port)
            return

        self.ports.remove(view_port)  # remove this port from the list
        # remove the token associated to x-window output
        token = self.tokens_by_port.pop(view_port)
        # stop the slot => render context / x-window mapping associated to the
        # token
        print(self.pre, "delViewPort: disconnecting token", token)
        openglthread.disconnect(token)
        print(self.pre, "delViewPort: OK disconnected token", token)
        self.x_screen_client(x_screen_num, inc = -1)
        
        
    def clearAllViewPorts(self):
        for port in copy.copy(self.ports):
            self.delViewPort(port)
            
        
    def setBoundingBoxes(self, view_port, bbox_list):
        x_screen_num = view_port.getXScreenNum()
        openglthread = self.openglthreads[x_screen_num]
        if (view_port in self.tokens_by_port):
            token = self.tokens_by_port[view_port]
            openglthread.core.clearObjectsCall(token)
            for bbox in bbox_list:
                openglthread.core.addRectangleCall(token, bbox[0], bbox[1], bbox[2], bbox[3]) # left, right, top, bottom


