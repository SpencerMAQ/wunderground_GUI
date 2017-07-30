import urllib.request
import csv
import os
import sys
from PyQt5.QtWidgets import (qApp, QAction, QMainWindow, QApplication,
                            QFileDialog, QPushButton, QTextEdit, QLabel,
                            QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFrame)
from PyQt5.QtCore import Qt

## sample address https://www.wunderground.com/history/airport/RPLL/2013/

class Importer(QWidget):

    def __init__(self):
        super(Importer, self).__init__()

        self.address_txt = QTextEdit(self)
        self.import_btn = QPushButton('Import')
        self.clr_btn = QPushButton('Clear')
        self.month_start = QSlider(Qt.Horizontal)
        self.month_end = QSlider(Qt.Horizontal)
        self.day_slider = QSlider(Qt.Horizontal)

        self.month_start.setMinimum(1)
        self.month_start.setMaximum(12)
        self.month_start.setTickInterval(1)
        self.month_start.setTickPosition(QSlider.TicksBelow)

        self.month_end.setMinimum(1)
        self.month_end.setMaximum(12)
        self.month_end.setTickInterval(1)
        self.month_end.setTickPosition(QSlider.TicksBelow)

        '''
        self.day_slider.setMinimum(1)
        self.day_slider.setMaximum(31)
        self.day_slider.setTickInterval(1)
        self.day_slider.setTickPosition(QSlider.TicksBelow)
        '''

        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        self.months_start = QLabel('Start = ' + str(self.month_start.value()))
        self.months_end = QLabel('Start = ' + str(self.month_start.value()))
        self.progress_label = QLabel('Progress')
        self.sample_site = QLabel(' Sample: https://www.wunderground.com/history/airport/RPLL/2013/')

        h_layout.addWidget(self.clr_btn)
        h_layout.addWidget(self.import_btn)

        v_layout.addWidget(self.sample_site)
        v_layout.addWidget(self.address_txt)
        v_layout.addWidget(self.month_start)
        v_layout.addWidget(self.months_start)   # Label
        v_layout.addWidget(self.month_end)
        v_layout.addWidget(self.months_end)     # Label

        v_layout.addWidget(self.progress_label)


        v_layout.addLayout(h_layout)

        self.import_btn.clicked.connect(self.import_data)
        self.clr_btn.clicked.connect(self.clear_text)
        self.month_start.valueChanged.connect(self.slider_change)
        self.month_end.valueChanged.connect(self.slider_change)


        self.setLayout(v_layout)

        self.show()

    def slider_change(self):
        self.months_start.setText('Start = ' + str(self.month_start.value()))
        self.months_end.setText('End = ' + str(self.month_end.value()))

    def import_data(self):

        filename = QFileDialog.getSaveFileName(self,
                                               'Save CSV',
                                               os.getenv('HOME'),
                                               'CSV *.csv'
                                               )
        x, y = 13, 32
        # x month, y days
        x_start = self.month_start.value()
        x_end = self.month_end.value() + 1    # +1 because range will end at number before last

        if filename[0] != '':
            with open(filename[0], "w") as file:
                print('Writing Data2')
                for i in range(x_start, x_end):
                    for j in range(y):
                        if i == 0 or j == 0:
                            continue

                        elif i == 2 and (j == 29 or j == 30 or j == 31): #Feb28
                            continue

                        elif i == 4 and (j == 31): #Apr30 (Apr = 4)
                            continue

                        elif i == 6 and (j == 31): #Jun30 (Jun = 6)
                            continue

                        elif i == 9 and (j == 31): #Sep30 (Sep = 9)
                            continue

                        elif i == 11 and (j == 31): #Nov30 (Nov = 11)
                            continue

                        else:
                            site = self.address_txt.toPlainText() + "{}/{}/DailyHistory.html?format=1".format(i, j)
                            #print(site)
                            self.progress_label.setText(site)

                        data = urllib.request.urlopen(site)

                        for l in data.readlines():
                            #writer.writerow(str(l) + "\n")
                            #writer.writerow(str(l))
                            #file.writelines(str(l) + "\n")
                            file.writelines(str(l) + "\n")

    def clear_text(self):
        self.text.clear()


class MenuBar(QMainWindow):

    def __init__(self):
        super(MenuBar, self).__init__()

        self.form_widget = Importer()
        self.setCentralWidget(self.form_widget)

        self.init_ui()

    def init_ui(self):
        bar = self.menuBar()

        file = bar.addMenu('File')

        import_action = QAction('Import', self)

        quit_action = QAction('&Quit', self)

        file.addAction(import_action)
        file.addAction(quit_action)

        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.respond)

        self.setWindowTitle('WUnderground Data Importer')

        self.show()

    @staticmethod
    def quit_trigger():
        qApp.quit()

    def respond(self, q):
        signal = q.text()

        if signal == 'Import':
            self.form_widget.import_data()
            print('import')

        else:
            pass


app = QApplication([])
importer = MenuBar()
sys.exit(app.exec_())