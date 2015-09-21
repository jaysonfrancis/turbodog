import sys
from PyQt4 import QtGui
from PyQt4.Qt import QTableWidget, QTableWidgetItem
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
#
class Window(QtGui.QMainWindow):    
    
    def __init__(self):
        super(Window, self).__init__()
     #   self.setGeometry(300, 300, 430, 150)  # (Position X, Position Y, Width, Height)
        self.setFixedSize(430,150)
        self.center()  # Custom method to center screen
        self.setWindowTitle('Children\'s Monitor (Senior Design 191)')  # Change title of window
        self.setWindowIcon(QtGui.QIcon('web.png'))  # Icon of the window
        self.statusBar().showMessage('Ready')  # First call of status bar method; Subsequent calls return the statusbar object 
        self.home()
               
    def home(self):     
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)  # Abstraction for actions performed with a menubar, toolbar, or shortcut
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.closeEvent)  # A triggered signal is emitted. The signal is connected to the quit() method which terminates application
        
        convertAction = QtGui.QAction(QtGui.QIcon('convert.png'), '&Convert', self)
        convertAction.setStatusTip('Convert Raw Data')
        convertAction.triggered.connect(self.convertData)
        
        uploadAction = QtGui.QAction(QtGui.QIcon('upload.png'), '&Upload', self)
        uploadAction.setStatusTip('Upload Data Online')
        uploadAction.triggered.connect(self.uploadData)
        
        emailAction = QtGui.QAction(QtGui.QIcon('email.png'), '&Email', self)
        emailAction.setStatusTip('Email Data')
        emailAction.triggered.connect(self.emailData)
        
        aboutAction = QtGui.QAction(QtGui.QIcon('help.png'), '&About', self)
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.aboutEvent)
        
        self.toolbar = self.addToolBar('Convert')
        self.toolbar.addAction(convertAction)
        
        self.toolbar = self.addToolBar('Upload')
        self.toolbar.addAction(uploadAction)
        
        self.toolbar = self.addToolBar('Email')
        self.toolbar.addAction(emailAction)
  
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)        
        
        
        menubar = self.menuBar()  # Create a menubar. Create a 'File' menu and append the exit action to the file menu.
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(convertAction)
        fileMenu.addAction(uploadAction)
        fileMenu.addAction(emailAction)
        fileMenu.addAction(exitAction)
        
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)
        
        
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(180,127,250,20)
              

        self.show()
           
    def convertData(self):
      self.completed = 0
      self.progress.setValue(self.completed)
      
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
 #     f = open(fname, 'r')
      
 #     with f:
 #       data = f.read()
 #       self.textEdit.setText(data)
      if fname:
        while self.completed < 100:
          self.completed += 0.0001
          self.progress.setValue(self.completed)
        else:
          self.statusBar().showMessage('Completed Conversion')

    
    # Method for emailing data
    def emailData(self):
      print "Email Data"  
      self.fileDialog = QtGui.QFileDialog(self)
      self.fileDialog.show()
    
    # Method for uploading data to cloud  
    def uploadData(self):
      print "Upload Data"  
      self.fileDialog = QtGui.QFileDialog(self)
      self.fileDialog.show() 
            
    # Method for window message box to verify exit
    def closeEvent(self, event):
      reply = QtGui.QMessageBox.question(self, 'Quit',
                                         "Are you sure you want to quit?",
                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      
      if reply == QtGui.QMessageBox.Yes: sys.exit()  # event.accept()
      else: event.ignore()
      
        # Method for window message box to verify exit
    def aboutEvent(self, event):
      QtGui.QMessageBox.question(self, 'About',
                                         "Version 1.0\n" +
                                         "Last Updated: 09/21/2015\n" +
                                         "Senior Design 191\n\n" +
                                         "Engineer: Jayson Francis\n" +
                                         "Contact: jaysonfrancis@gmail.com",
                                         QtGui.QMessageBox.Ok)
  
      
    # Method to center the application on the screen
    def center(self):
      qr = self.frameGeometry()  # Get a rectangle specifying the geometry of the main window. This includes any window frame.
      cp = QtGui.QDesktopWidget().availableGeometry().center()  # Figure out the screen resolution of the monitor and get the center point
      qr.moveCenter(cp)  # Set the center of rectangle to the center of the screen. 

      
      
      
      
      
      
      
      
      
      
      
      self.move(qr.topLeft())  # Move the top-left point of application window to top-left point of the qr rectangle, thus centering the screen
                  
def main():    
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
