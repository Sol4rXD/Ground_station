import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

# Set serial
PORT_NAME = 'COM5'
BAUDRATE  = '115200'
# ser = serial.Serial(PORT_NAME, BAUDRATE)

# Set colour background
colour_background = 'black'   

# Set colour line
colour_line = 'cyan'     

# Set title of GUI
gui_title = 'GUI Test'

pg.setConfigOptions(antialias=True)

def create_ui():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)

    # Create a window with a plot area
    win = pg.GraphicsLayoutWidget()
    win.setWindowTitle(gui_title)
    win.resize(900, 700)

    # Set colour of background
    win.setBackground(colour_background)

    # Add two rows of plots to the window
    top_row = win.addLayout(row=0, col=0)
    middle_row = win.addLayout(row=1, col=0)
    bottom_row = win.addLayout(row=2, col=0)

    # plots 1
    plot1 = top_row.addPlot(title="Data 1")
    plot1.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot1.setTitle('<span style="color: black;">Data 1</span>')
    plot1.setLabel('bottom', 'Time (s)')
    plot1.setLabel('left', 'Y Label')
    plot1.showGrid(x=True, y=True)

    # plots 2
    plot2 = top_row.addPlot(title="Data 2")
    plot2.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot2.setTitle('<span style="color: black;">Data 2</span>')
    plot2.setLabel('bottom', 'Time (s)')
    plot2.setLabel('left', 'Y Label')
    plot2.showGrid(x=True, y=True)

    # plots 3
    plot3 = middle_row.addPlot(title="Data 3")
    plot3.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot3.setTitle('<span style="color: black;">Data 3</span>')
    plot3.setLabel('bottom', 'Time (s)')
    plot3.setLabel('left', 'Y Label')
    plot3.showGrid(x=True, y=True)

    # plots 4
    plot4 = middle_row.addPlot(title="Data 4")
    plot4.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot4.setTitle('<span style="color: black;">Data 4</span>')
    plot4.setLabel('bottom', 'Time (s)')
    plot4.setLabel('left', 'Y Label')
    plot4.showGrid(x=True, y=True)

    # plots 5
    plot5 = bottom_row.addPlot(title ="Data 5")
    plot5.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot5.setTitle('<span style="color: black;">Data 5</span>')
    plot5.setLabel('bottom', 'Time (s)')
    plot5.setLabel('left', 'Y Label')
    plot5.showGrid(x=True, y=True)

    # plots 6
    plot6 = bottom_row.addPlot(title ="Data 6")
    plot6.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], pen=pg.mkPen(color=colour_line, width=1.25))
    plot6.setTitle('<span style="color: black;">Data 6</span>')
    plot6.setLabel('bottom', 'Time (s)')
    plot6.setLabel('left', 'Y Label')
    plot6.showGrid(x=True, y=True)

    # Show the window
    win.show()

    print('The graph is showing')

    sys.exit(app.exec_())

create_ui()




