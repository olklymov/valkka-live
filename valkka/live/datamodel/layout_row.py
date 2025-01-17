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


::

            {'valkka.live.container.grid.VideoContainerNxM': [
                {   # individual serialized container
                    'child_class': <class 'valkka.live.container.video.VideoContainer'>,
                    'child_pars': [{'device_id': -1}],
                    'geom': (604, 0, 300, 300),
                    'm_dim': 1,
                    'n_dim': 1,
                    'n_xscreen': 0,
                    'title': 'Video Grid'
                },
                ...
                ]
            }

"""

import sys
from valkka.live.qimport import QtWidgets, QtCore, QtGui, Signal, Slot  # Qt5
from cute_mongo_forms.column import Column, ForeignKeyColumn
from cute_mongo_forms.row import ColumnSpec, Row
#from cute_mongo_forms.container import List, SimpleForm
from valkka.live import default, tools

""" not really needed..
class VideoContainerNxMRow(Row):
    name = "VideoContainerNxM"
    columns = [
        ColumnSpec(Column,  # child class name as string
            key_name="child_class"),
        ColumnSpec(Column,  # child parameters: a list of dicts
            key_name="child_pars"),
        ColumnSpec(Column,  # a tuple
            key_name="geom"),
        ColumnSpec(Column,
            key_name="m_dim"),
        ColumnSpec(Column,
            key_name="n_dim"),
        ColumnSpec(Column,
            key_name="title"),
        ColumnSpec(Column,
            key_name="n_xscreen"),
        #ColumnSpec(ForeignKeyColumn,
        #    key_name="group_id")
        ]

# VideoContainerNxMRow, PlayVideoContainerNxMRow, CameraListWindowRow, MainWindowRow

class PlayVideoContainerNxMRow(VideoContainerNxMRow):
    name = "PlayVideoContainerNxM"


class WindowRow(Row):
    name = "Window"
    columns = [
        ColumnSpec(Column,  # a tuple
            key_name="geom"),
        ColumnSpec(Column,
            key_name="title"),
        ColumnSpec(Column,
            key_name="n_xscreen"),
        #ColumnSpec(ForeignKeyColumn,
        #    key_name="group_id")
        ]

class CameraListWindowRow(WindowRow):
    name = "CameraListWindow"

class MainWindowRow(Row):
    name = "MainWindow"
"""

class LayoutContainerRow(Row):
    name = "LayoutContainer"
    columns = [
        ColumnSpec(Column,  # just a list of json objects :)
            key_name="layout"),
    ]




class MyGui(QtWidgets.QMainWindow):

  
  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    self.openValkka()
    

  def initVars(self):
    pass


  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,500,500))
    
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    
    
  def openValkka(self):
    pass
    
  
  def closeValkka(self):
    pass
  
  
  def closeEvent(self,e):
    print("closeEvent!")
    self.closeValkka()
    e.accept()



def main():
  app=QtWidgets.QApplication(["test_app"])
  mg=MyGui()
  mg.show()
  app.exec_()



if (__name__=="__main__"):
  main()
 
