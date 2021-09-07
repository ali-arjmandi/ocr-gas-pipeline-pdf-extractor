from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, pytesseract, sys, threading, cv2, numpy, pyodbc
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
from pdf_to_df import *
import numpy as np
import pandas as pd
from add_view import Ui_add_view

conn = ''

class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class Project(QtWidgets.QMainWindow, Ui_add_view):
    progressChanged = QtCore.pyqtSignal(int)

    def __init__(self, dialog):
        QtWidgets.QMainWindow.__init__(self)
        dialog = dialog
        dialog.setFixedSize(952, 562)
        Ui_add_view.setupUi(self, dialog)
        self.setup_add()
        self.disable_stylesheet((self.btn_delete,self.btn_start))
        self.table_sheet.setVisible(False)
        self.table_line.setVisible(False)
        self.working = False
        self.finished = False
        self.waiting = False
        self.start = False
        self.names = []

#  =================================================================

    def setup_add(self):
        self.btn_tak_of.mousePressEvent = self.tak_of_act
        self.btn_sheet.mousePressEvent = self.sheet_act
        self.btn_line.mousePressEvent = self.line_act
        self.btn_load.mousePressEvent = self.load_act
        self.btn_delete.mousePressEvent = self.delete_act
        self.btn_start.mousePressEvent = self.start_act
        self.listView.clicked.connect(self.setup_table)
        self.progressChanged.connect(self.progressBar.setValue)

#  =================================================================
    def tak_of_act(self, event):
        self.table_tak_of.setVisible(True)
        self.table_sheet.setVisible(False)
        self.table_line.setVisible(False)
        self.btn_tak_of.setStyleSheet(
        """background-color:#dedede;
        border:2px solid #2f419b;
        color:#2f419b;""")
        self.btn_sheet.setStyleSheet('')
        self.btn_line.setStyleSheet('')

    def sheet_act(self, event):
        self.table_tak_of.setVisible(False)
        self.table_sheet.setVisible(True)
        self.table_line.setVisible(False)
        self.btn_sheet.setStyleSheet(
        """background-color:#dedede;
        border:2px solid #2f419b;
        color:#2f419b;""")
        self.btn_tak_of.setStyleSheet('')
        self.btn_line.setStyleSheet('')

    def line_act(self, event):
        self.table_tak_of.setVisible(False)
        self.table_sheet.setVisible(False)
        self.table_line.setVisible(True)
        self.btn_line.setStyleSheet(
        """background-color:#dedede;
        border:2px solid #2f419b;
        color:#2f419b;""")
        self.btn_tak_of.setStyleSheet('')
        self.btn_sheet.setStyleSheet('')

    def load_act(self, event):
        list = QFileDialog.getOpenFileNames(None,"Open PDF File", '.',  "PDF files (*.pdf)")[0]
        for str in list:
            self.names.append(str)
            item = QtWidgets.QListWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(str.split('/')[-1])
            self.listView.addItem(item)
        if len(self.names)>0:
            self.btn_delete.setEnabled(True)
            self.btn_start.setEnabled(True)
            self.enable_stylesheet((self.btn_delete,self.btn_start))

    def delete_act(self, event):
        listItems=self.listView.selectedItems()
        if not listItems: return
        for item in listItems:
            index = self.listView.row(item)
            self.listView.takeItem(index)
            del self.names[index]
            if self.finished:
                del self.data_list[index]
        if len(self.names)==0:
            self.btn_delete.setEnabled(False)
            self.btn_start.setEnabled(False)
            self.disable_stylesheet((self.btn_delete,self.btn_start))

    def start_act(self, event):
        if not self.finished:
            if self.working:
                if self.start:
                    if not self.waiting:
                        self.e.set()
                        self.waiting = True
                        self.btn_start.setText('...')
                        self.pause_stylesheet()

                else:
                    self.start = True
                    self.btn_start.setText('Pause')
                    self.e.set()

            else:
                self.e = threading.Event()
                self.listView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                self.working = True
                self.start = True
                self.progressBar.setEnabled(True)
                self.btn_delete.setEnabled(False)
                self.btn_load.setEnabled(False)
                self.disable_stylesheet((self.btn_delete,self.btn_load))
                self.btn_start.setText('Pause')
                self.t = threading.Thread(target=self.start_thread)
                self.t.setDaemon(True)
                self.t.start()                
        else:
            self.names = []
            self.data_list = []
            self.listView.clear()
            self.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            self.finished = False
            self.start = False
            self.working = False
            self.btn_load.setEnabled(True)
            self.btn_start.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self.enable_stylesheet((self.btn_load,))
            self.disable_stylesheet((self.btn_delete,self.btn_start))
            self.progressBar.setValue(0)
            self.btn_start.setText('Start')
            model = PandasModel(pd.DataFrame())
            self.table_tak_of.setModel(model)
            self.table_sheet.setModel(model)
            self.table_line.setModel(model)
            self.progressBar.setStyleSheet("")
            
            

    def start_thread(self):
        global conn
        index = 0
        l = len(self.names)
        p = 100 / (l*4)
        progress = 0
        self.data_list = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path += "\\db_config.txt"
        file = open(dir_path,'r')
        conf=file.read()
        file.close()
        conn = pyodbc.connect(conf)
        cursor = conn.cursor()

        for src in self.names:
            src = '\\'.join(src.split('/'))
            flag = False
            input1 = PdfFileReader(open(src, 'rb'))
            if input1.getNumPages() != 1:
                progress += 4*p
                self.progressChanged.emit(progress)
                self.data_list.append(())
                index += 1
                continue
            if input1.getPage(0).mediaBox[2] < 1800:
                dpi = 290
                flag = True
            else:
                dpi = 160
            img = convert_from_path(src, dpi=dpi)[0]
            img = np.array(img) 
            img = img[:, :, ::-1].copy()
            bw = threshold(img) 

            v = vertical(bw, 20)
            if main_area(v, img) != 404:
                new_img, line_x = main_area(v, img)
            else:
                progress += 4*p
                self.progressChanged.emit(progress)
                self.data_list.append(())
                index += 1
                continue
            if self.e.isSet():
                self.e.clear()
                self.waiting = False
                self.start = False
                self.btn_start.setText('Resume')
                self.e.wait()
                self.start = True
                self.resume_stylesheet()
                self.e.clear()
            progress += p
            self.progressChanged.emit(progress)
            new_bw = threshold(new_img)
            h = horizontal(new_bw, 20)
            kernel = np.ones((2,2),np.uint8)
            new_bw = cv2.dilate(new_bw,kernel,iterations = 1)
            new_img = del_text(h, new_bw, line_x)
            new_img = cv2.bitwise_not(new_img)
            str = pytesseract.image_to_data(new_img,config='--psm 6 -c textord_old_xheight=1  -c tessedit_char_blacklist=([/|\\\"—_])')
            tak_of = analize_right(str, new_img.shape)
            if self.e.isSet():
                self.e.clear()
                self.waiting = False
                self.start = False
                self.btn_start.setText('Resume')
                self.e.wait()
                self.start = True
                self.resume_stylesheet()
                self.e.clear()
            progress += p
            self.progressChanged.emit(progress)
            h = horizontal(bw, 10)
            v = vertical(bw, 40)
            new_img, M = cut(h,v,img)
            str1 = pytesseract.image_to_data(new_img[:,:int(new_img.shape[1]/2)], config='--psm 6 -c textord_old_xheight=1 -c tessedit_char_blacklist=|[]l—')
            if flag:
                new_img = cv2.blur(new_img,(1,1))
                new_img = cv2.adaptiveThreshold(
                    new_img, 255,
                    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                    25,
                    25
                )
                new_img = cv2.bitwise_not(new_img)
            if self.e.isSet():
                self.e.clear()
                self.waiting = False
                self.start = False
                self.btn_start.setText('Resume')
                self.e.wait()
                self.start = True
                self.resume_stylesheet()
                self.e.clear()
            progress += p
            self.progressChanged.emit(progress)
            str2 = pytesseract.image_to_data(new_img[:,int(new_img.shape[1]/2):], config='--psm 6 -c tessedit_char_blacklist=|[]l— ')
            values = analize_down(str1, str2, new_img.shape, M)
            line, sheet = find_element(values, src.split('\\')[-1], new_img.shape)
            self.data_list.append((tak_of, sheet, line))
            if self.e.isSet():
                self.e.clear()
                self.waiting = False
                self.start = False
                self.btn_start.setText('Resume')
                self.e.wait()
                self.start = True
                self.resume_stylesheet()
                self.e.clear()
            try:
                cursor.execute("INSERT INTO dbo.Line (LineNum, DocumentNo, DrawingNo, LineClass, UnitNo, PIDNo,PressDesign,TempDesign,PressOperating,TempOperating,TestFluid,PressTest,InsualtionType,InsulationThk,PaintCode,HeatTransfer,StressAnalysis,Density,SteamTracing,TracingSize,ElecTracing,NDT,PWHT,Phase,Rev,SHEETS) VALUES (\'{}\');".format("\',\'".join(line.values.tolist()[0])))
                val = cursor.execute("SELECT IDENT_CURRENT('dbo.Line');") 
                val = int(val.fetchone()[0])
                cursor.execute("INSERT INTO dbo.sheet (id_line, SheetNum, Of_, Rev, DocClass) VALUES (\'{}\',\'{}\');".format(val,"\',\'".join(sheet.values.tolist()[0])))
                for row in tak_of.values.tolist():
                    cursor.execute("INSERT INTO dbo.tak_of (id_line, PTNo, ItemCode, Qty, Type) VALUES (\'{}\',\'{}\');".format(val,"\',\'".join(row)))
                cursor.commit() 
            except:
                pass
            progress += p
            self.progressChanged.emit(progress)
            self.listView.item(index).setCheckState(True)
            index += 1

        conn.close()
        conn = ''
        self.progressChanged.emit(100)
        self.btn_start.setText('Restart')
        self.finished = True
        self.progressBar.setStyleSheet("QProgressBar::chunk:horizontal{\n"
                                            "background:  rgb(1, 97, 44);\n"
                                            "border-radius:6px;}\n")

    def setup_table(self, event):
        if self.working or self.finished:
            index = self.listView.selectedItems()[0]
            index = self.listView.row(index)
            if self.listView.item(index).checkState():
                if len(self.data_list[index]):
                    model = PandasModel(self.data_list[index][0])
                    self.table_tak_of.setModel(model)
                    model = PandasModel(self.data_list[index][1])
                    self.table_sheet.setModel(model)
                    model = PandasModel(self.data_list[index][2])
                    self.table_line.setModel(model)
            else:
                model = PandasModel(pd.DataFrame())
                self.table_tak_of.setModel(model)
                self.table_sheet.setModel(model)
                self.table_line.setModel(model)
        

    def disable_stylesheet(self,tuples):
        for i in tuples:
            i.setStyleSheet("background-color: rgb(200, 200, 200);\n"
                                "border-radius:25px;\n"
                                "color:white;\n")
    def enable_stylesheet(self,tuples):
        for i in tuples:
            i.setStyleSheet("")
    def pause_stylesheet(self):
            self.progressBar.setStyleSheet("QProgressBar::chunk:horizontal{\n"
                                            "background:  #e38108;\n"
                                            "border-radius:6px;}\n")
            self.btn_start.setStyleSheet("background: #e38108\n")
    def resume_stylesheet(self):
            self.progressBar.setStyleSheet("")
            self.btn_start.setStyleSheet("")


def main():
    global conn
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    Project(dialog)
    dialog.show()
    app.exec_()
    print(conn)
    if conn != '':
        conn.close()
if __name__ == '__main__':
    main()
