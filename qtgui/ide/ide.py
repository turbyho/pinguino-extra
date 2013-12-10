#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import codecs

from PySide import QtGui, QtCore

from .helpers.backgrounds import BackgroundPallete
from .features.features import PinguinoFeatures
from .helpers import constants as Constants
from .helpers.dialogs import Dialogs
from .helpers.stdout_stderr_manager import StdeOut, StdErr
from .helpers.config import Config
from ..frames.main import Ui_PinguinoIDE
from pinguino.pinguino import Pinguino, AllBoards

########################################################################
class PinguinoIDE(QtGui.QMainWindow, PinguinoFeatures):
    def __init__(self):
        super(PinguinoIDE, self).__init__()
        
        self.main= Ui_PinguinoIDE()          
        self.main.setupUi(self)
        self.setWindowTitle(Constants.TAB_NAME)
        
        self.fix_palettes()
        self.__initialize_features__()
        
        self.connect_events()
        self.main.tabWidget_files.setVisible(False)
        
        self.pinguinoAPI = Pinguino()
        self.configIDE = Config()
        setattr(self.pinguinoAPI, "_boards_", AllBoards)
        
        self.redirect_this = None

        self.main.toolBar_graphical.setVisible(False)
    
        self.update_functions()
        self.update_directives()
        self.update_variables()
        self.__update_path_files__(Constants.PINGUINO_EXAMPLES_DIR)
        self.__update_graphical_path_files__(Constants.PINGUINOG_EXAMPLES_DIR)
        
        self.set_board()
        self.statusbar_ide(self.get_description_board())
        
                    
        #self.main.plainTextEdit_output.write = self.main.plainTextEdit_output.appendPlainText
        #self.install_out_redirect()
        #self.install_error_redirect()
         
        
        
    ##----------------------------------------------------------------------
    #def install_out_redirect(self):
        #""""""
        #sys.stdout = self.main.plainTextEdit_output
        
        
    ##----------------------------------------------------------------------
    #def install_error_redirect(self, popup=False):
        #""""""
        #sys.stderr = self.main.plainTextEdit_output

    #----------------------------------------------------------------------
    def output_ide(self, *args, **kwargs):
        """"""
        for line in args:
            self.main.plainTextEdit_output.appendPlainText(line)
            
        for key in kwargs.keys():
            line = key + ": " + kwargs[key]
            self.main.plainTextEdit_output.appendPlainText(line)
        
    #----------------------------------------------------------------------
    def clear_output_ide(self):
        """"""
        self.main.plainTextEdit_output.setPlainText("")
        
    #----------------------------------------------------------------------
    def statusbar_ide(self, status):
        """"""
        self.main.actionBoard_info.setText(status)
        
    #----------------------------------------------------------------------
    def set_board(self):
        """"""
        board_name = self.configIDE.config("Board", "board", "Pinguino 2550")
        for board in self.pinguinoAPI._boards_:
            if board.name == board_name:
                self.pinguinoAPI.set_board(board)
        
        arch = self.configIDE.config("Board", "arch", 8)        
        if arch == 8:
            bootloader = self.configIDE.config("Board", "bootloader", "v1_v2")
            if bootloader == "v1_v2":
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot2)
            else:
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot4)
                
                
    #----------------------------------------------------------------------
    def get_description_board(self):
        """"""
        board = self.pinguinoAPI.get_board()
        board_config = "Board: %s\n" % board.name
        board_config += "Proc: %s\n" % board.proc
        board_config += "Arch: %s\n" % board.arch
        
        if board.arch == 8 and board.bldr == "boot4":
            board_config += "Boootloader: v4\n"
        if board.arch == 8 and board.bldr == "boot2":
            board_config += "Boootloader: v1 & v2\n"
            
        return board_config
    
    

    #----------------------------------------------------------------------
    def fix_palettes(self):
        """"""
        pallete = BackgroundPallete()
        pallete.save_palette(self.main.centralwidget.parent())

        pallete.set_background_pinguino(self.main.dockWidget_output)
        pallete.set_background_pinguino(self.main.dockWidget_tools)
        pallete.set_background_pinguino(self.main.dockWidget_blocks)  
        pallete.set_background_pinguino(self.main.toolBar_board)
        pallete.set_background_pinguino(self.main.centralwidget.parent())
        
        
        pallete.set_default_palette(self.main.toolBar_edit)
        pallete.set_default_palette(self.main.toolBar_files)
        pallete.set_default_palette(self.main.toolBar_search_replace)
        pallete.set_default_palette(self.main.toolBar_undo_redo)
        pallete.set_default_palette(self.main.toolBar_pinguino)
        pallete.set_default_palette(self.main.toolBar_graphical)
        pallete.set_default_palette(self.main.toolBar_switch)
        
        
        #pallete.set_default_palette(self.main.toolBar_switch)     