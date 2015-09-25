import sys, csv, os, xlsxwriter
from PyQt4 import QtGui
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import plotly.plotly as py
from plotly.graph_objs import *

class Window(QtGui.QMainWindow):    
    
    def __init__(self):
        super(Window, self).__init__()
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
        uploadAction.setStatusTip('Interactive Chart (Plotly)')
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
      print fname # Debug
      
      workbook = xlsxwriter.Workbook("test.xlsx", {'strings_to_numbers': True})
      
      chartworksheet = workbook.add_worksheet("Charts")
      dataworksheet = workbook.add_worksheet("Data")

      self.statusBar().showMessage('Reading data....')
      with open (fname, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
          for c, col in enumerate(row):
              dataworksheet.write(r, c, col)
              updateProgress(self)

      self.statusBar().showMessage('Setting up charts...')
      chart = workbook.add_chart({'type': 'line'})
      chart.set_size({'width': 1400, 'height': 900})
      chart.set_legend({'position': 'bottom'})
      chart.set_plotarea({
                          'border': {'color': 'red', 'width': 2, 'dash_type': 'dash'},
                          'fill':   {'color': '#FFFFC2'}
    })  
      chart.set_title({
                       'name': 'Monitor',
                       'name_font': {
                                     'name': 'Calibri',
                                     'color': 'blue',
                                     },
                       })
      chart.set_x_axis({
                        'name': 'Timestamp',
                 #       'position_axis': 'on_tick',
                 #       'date_axis': True,
                        'name_font': {
                                      'name': 'Courier New',
                                      'color': '#92D050'
                                      },
                        'num_font': {
                                     'name': 'Arial',
                                     'color': '#00B0F0',
                                     },
                        })
    
      chart.add_series({'values': '=Data!$B$2:$B$58000', 'categories': '=Data!$A$1:$A$58000', 'name': 'X-Axis'})
      chart.add_series({'values': '=Data!$C$2:$C$58000', 'categories': '=Data!$A$1:$A$58000', 'name': 'Y-Axis'})
      chart.add_series({'values': '=Data!$D$2:$D$58000', 'categories': '=Data!$A$1:$A$58000', 'name': 'Z-Axis'})
      
      chartworksheet.insert_chart('A1', chart)
      workbook.close()

      if fname:
        while self.completed < 100:
          self.completed += 0.0001
          self.progress.setValue(self.completed)
        else:
          self.statusBar().showMessage('Completed Conversion')

      os.system("test.xlsx")
   
    # Method for emailing data
    def emailData(self):
      print "Email Data"  
      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
      print fname # Debug

    # Method for uploading data to cloud  
    def uploadData(self):
      self.completed = 0
      self.progress.setValue(self.completed)

      fname = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
      print fname # Debug
      self.statusBar().showMessage('Uploading data. Please wait...')
      def getColumn(filename, column):
        results = csv.reader(open(filename, 'rU'), delimiter=",")
        return [result[column] for result in results]

      timestamp = getColumn(fname,0)
      xaxis = getColumn(fname,1)
      yaxis = getColumn(fname,2)
      zaxis = getColumn(fname,3)

      trace1 = Scatter(
        x=timestamp,
        y=xaxis,
        name='x-axis',
        marker=Marker(color='rgb(55, 83, 109)')
        )

      trace2 = Scatter(
        x=timestamp,
        y=yaxis,
        name='y-axis',
        marker=Marker(color='rgb(234, 153, 153)')
        )
      trace3 = Scatter(
        x=timestamp,
        y=zaxis,
        name='z-axis',
        marker=Marker(color='green')
        )

      layout = Layout(
        title='Data Analysis',
        xaxis=XAxis(
        showgrid=False,
        ),
        yaxis=YAxis(
        title='Points',
        showline=False
        ),
        barmode='group'
 
        )
      data = Data([trace1, trace2, trace3])

      fig = Figure(data=data, layout=layout)
      plot_url = py.plot(fig, filename='output')
      print plot_url
      
      self.statusBar().showMessage('Upload Complete.')   
      self.progress.setValue(100)
      
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

def updateProgress(self):
    if self.completed < 100:
      self.completed += 0.0001 
      self.progress.setValue(self.completed)
    else: 
      self.statusBar().showMessage('Completed Conversion')           

                     
def main():    
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
