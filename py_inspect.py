from PyQt5.QtCore import QLocale
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton 
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QMessageBox  
import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
# fix imports
import time
import threading
import win32api
from pywinauto import backend
import pywinauto
import inspect

# rewrite with hooks + find in tree
def lookForMouse(w):
    desktop = pywinauto.Desktop(backend='uia')
    while True:
        time.sleep(0.5)
        if w.mouse.isChecked():
            x, y = win32api.GetCursorPos()
            desktop.from_point(x, y).draw_outline()

# TODO check all in win32
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = MyWindow()
    w.show()
    #x = threading.Thread(target=lookForMouse, args=(w,), daemon=True)
    # x.start()
    sys.exit(app.exec_())

class InfoDialog(QDialog):
    def __init__(self, title, items, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        listView = QListView()
        model = QStandardItemModel()
        listView.setModel(model)

        for item in items:
            model.appendRow(QStandardItem(str(item)))

        self.layout = QGridLayout()
        self.layout.addWidget(listView)
        self.setLayout(self.layout)
        self.resize(400, 300)

class ClickInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.button = QGroupBox("button")
        self.left = QRadioButton("left")
        self.right = QRadioButton("right")
        self.middle = QRadioButton("middle")
        self.coords = QGroupBox("coords")
        self.x = QLineEdit()
        self.x.setValidator(QIntValidator())
        self.y = QLineEdit()
        self.y.setValidator(QIntValidator())
        self.double = QCheckBox('double')
        self.wheel = QGroupBox('wheel_dist')
        self.wheel_dist = QLineEdit()
        self.wheel_dist.setValidator(QIntValidator())
        self.confirm = QPushButton('confirm')
        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('click_input()')

        grid = QGridLayout()

        self.button.setFont(QFont("Sanserif", 14))

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.left)
        vbox1.addWidget(self.right)
        vbox1.addWidget(self.middle)

        vbox1.addStretch(1)
        self.button.setLayout(vbox1)

        self.coords.setFont(QFont("Sanserif", 14))

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.x)
        vbox2.addWidget(self.y)

        vbox2.addStretch(1)
        self.coords.setLayout(vbox2)

        self.double.setChecked(False)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.wheel_dist)

        #vbox3.addStretch(1)
        self.wheel.setLayout(vbox3)

        grid.addWidget(self.button, 0, 0)
        grid.addWidget(self.coords, 0, 1)
        grid.addWidget(self.double, 1, 0)
        grid.addWidget(self.wheel, 1, 1)
        grid.addWidget(self.confirm, 2, 0, 1, 2)

        self.setLayout(grid)

        self.resize(400, 300)

        self.confirm.clicked.connect(self.win_close)

    def win_close(self):
        if self.x.text()=='' and self.y.text()!='' or self.x.text()!='' and self.y.text()=='':
            QMessageBox.warning(self, "Attention", "Please type coords correctly!")
        else:
            self.close()

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Methods
        #print(set([attr for attr in dir(pywinauto.base_wrapper.BaseWrapper)if not attr.startswith('_')]))
        self.base_methods = {'capture_as_image': self.__capture_as_image, 'children': self.__children, 'click_input': self.__click_input, 'close': self.__close, 'descendants': self.__descendants, 'draw_outline': self.__draw_outline, 'set_focus': self.__set_focus, 'texts': self.__texts,
                             'type_keys': self.__type_keys, 'wait_enabled': self.__wait_enabled, 'wait_not_enabled': self.__wait_not_enabled, 'wait_not_visible': self.__wait_not_visible, 'wait_visible': self.__wait_visible, 'window_text': self.__window_text}

        self.setMinimumSize(1000, 500)
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.setWindowTitle(
            QCoreApplication.translate("MainWindow", "PyInspect"))

        self.settings = QSettings('py_inspect', 'MainWindow')

        # Main layout
        self.mainLayout = QGridLayout()

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.action = self.menu_bar.addMenu("Actions")
        refresh = QAction('Refresh', self)
        refresh.triggered.connect(self.__refresh)
        self.mouse = QAction('Find by mouse', self)
        self.mouse.setCheckable(True)
        default = QAction('Default Action', self)
        default.triggered.connect(self.__default)
        self.action.addAction(refresh)
        self.action.addAction(self.mouse)
        self.action.addAction(default)
        self.action.addSeparator()
        self.bmethods = self.action.addMenu("Base Methods")
        # (uia_defines.py/_build_pattern_ids_dic)
        self.cmethods = self.action.addMenu('Current Elem Methods')

        # Backend label
        self.backendLabel = QLabel("Backend Type")

        # Backend combobox
        self.comboBox = QComboBox()
        self.comboBox.setMouseTracking(False)
        self.comboBox.setMaxVisibleItems(5)
        self.comboBox.setObjectName("comboBox")

        for _backend in backend.registry.backends.keys():
            self.comboBox.addItem(_backend)

        # Add top widgets to main window
        self.mainLayout.addWidget(self.menu_bar, 0, 0)
        self.mainLayout.addWidget(self.backendLabel, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.tree_view = QTreeView()
        self.tree_view.setColumnWidth(0, 150)

        self.comboBox.setCurrentText('uia')
        self.current_elem_wrapper = None
        self.__initialize_calc()

        self.table_view = QTableView()

        self.comboBox.activated[str].connect(self.__show_tree)

        # Add center widgets to main window
        self.mainLayout.addWidget(self.tree_view, 2, 0, 1, 1)
        self.mainLayout.addWidget(self.table_view, 2, 1, 1, 1)

        self.setLayout(self.mainLayout)
        geometry = self.settings.value('Geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)

    def __initialize_calc(self, _backend='uia'):
        self.element_info \
            = backend.registry.backends[_backend].element_info_class()
        self.tree_model = MyTreeModel(self.element_info, _backend)
        self.tree_model.setHeaderData(0, Qt.Horizontal, 'Controls')
        self.tree_view.setModel(self.tree_model)
        self.tree_view.clicked.connect(self.__show_property)

    def __show_tree(self, text):
        backend = text
        self.current_elem_wrapper = None
        self.__initialize_calc(backend)

    def __show_property(self, index=None):
        data = index.data()
        self.current_elem_info = self.tree_model.info_dict.get(data)
        if self.comboBox.currentText() == 'win32':
            self.current_elem_wrapper = pywinauto.controls.hwndwrapper.HwndWrapper(
                self.current_elem_info)
        elif self.comboBox.currentText() == 'uia':
            self.current_elem_wrapper = pywinauto.controls.uiawrapper.UIAWrapper(
                self.current_elem_info)
            # autogenerate methods
            self.bmethods.clear()
            for method in self.base_methods.keys():
                action = QAction(method + '()', self)
                action.triggered.connect(self.base_methods[method])
                self.bmethods.addAction(action)
        # Debug
        print(self.current_elem_wrapper)
        # Unique methods
        # print(set([attr for attr in dir(self.current_elem_wrapper)if not attr.startswith('_') and not attr.startswith('iface_') and inspect.ismethod(getattr(self.current_elem_wrapper, attr))])-set([method for method in self.base_methods.keys()])-set([prop[0] for prop in self.tree_model.props_dict.get(data)]))
        # Not overrided methods
        # print(set([method for method in self.base_methods.keys()])-set([attr for attr in dir(self.current_elem_wrapper)])&set([method for method in self.base_methods.keys()]))
        # Not showing properties
        # print(set([attr for attr in dir(self.current_elem_info)if not attr.startswith('_') and not inspect.ismethod(getattr(self.current_elem_info,attr))])-set([prop[0] for prop in self.tree_model.props_dict.get(data)]))

        self.table_model \
            = MyTableModel(self.tree_model.props_dict.get(data), self)
        self.table_view.wordWrap()
        self.table_view.setModel(self.table_model)
        self.table_view.setColumnWidth(1, 320)

    # Actions
    def __refresh(self):
        self.current_elem_wrapper = None
        self.__initialize_calc(str(self.comboBox.currentText()))

    def __default(self):
        if self.comboBox.currentText() == 'uia':
            if self.current_elem_info.legacy_action != '':
                self.current_elem_wrapper.iface_legacy_iaccessible.DoDefaultAction()
            else:
                self.current_elem_wrapper.set_focus()
        else:
            pass

    # Base Methods
    def __capture_as_image(self):
        img = self.current_elem_wrapper.capture_as_image()
        if img != None:
            img.show()
        else:
            print('can not capture as image')

    def __children(self):
        dlg=InfoDialog('children()', self.current_elem_wrapper.children(), self)
        dlg.exec()


    def __click_input(self):
        dlg=ClickInput(self)
        dlg.exec()
        button = 'left'
        coords=(None,None)
        double = False
        wheel_dist = 0
        if dlg.right.isChecked():
            button='right'
        elif dlg.middle.isChecked():
            button='middle'
        if dlg.x.text()!='':
            coords=(int(dlg.x.text()),int(dlg.y.text()))
        if dlg.double.isChecked():
            double=True
        if dlg.wheel_dist.text()!='':
            wheel_dist=int(dlg.wheel_dist.text())
        self.current_elem_wrapper.click_input(button=button, coords=coords, double=double, wheel_dist=wheel_dist)
    
    def __close(self):
        if self.current_elem_wrapper:
            if self.current_elem_wrapper.is_dialog():
                self.current_elem_wrapper.close()
                self.__refresh()

    def __descendants(self):
        dlg=InfoDialog('descendants()', self.current_elem_wrapper.descendants(), self)
        dlg.exec()

    def __draw_outline(self):
        self.current_elem_wrapper.draw_outline()

    def __set_focus(self):
        self.current_elem_wrapper.set_focus()

    def __texts(self):
        dlg=InfoDialog('texts()', self.current_elem_wrapper.texts(), self)
        dlg.exec()

    def __type_keys(self):
        # show dialog to choose keys
        self.current_elem_wrapper.type_keys()

    def __wait_enabled(self):
        self.current_elem_wrapper.wait_enabled()

    def __wait_not_enabled(self):
        self.current_elem_wrapper.wait_not_enabled()

    def __wait_not_visible(self):
        self.current_elem_wrapper.wait_not_visible()

    def __wait_visible(self):
        self.current_elem_wrapper.wait_visible()

    def __window_text(self):
        dlg=InfoDialog('window_text', [self.current_elem_wrapper.window_text()], self)
        dlg.exec()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('Geometry', geometry)
        super(MyWindow, self).closeEvent(event)


class MyTreeModel(QStandardItemModel):
    def __init__(self, element_info, backend):
        QStandardItemModel.__init__(self)
        root_node = self.invisibleRootItem()
        self.props_dict = {}
        self.info_dict = {}
        self.backend = backend
        self.branch = QStandardItem(self.__node_name(element_info))
        self.branch.setEditable(False)
        root_node.appendRow(self.branch)
        self.__generate_props_dict(element_info)
        self.__get_next(element_info, self.branch)

    def __get_next(self, element_info, parent):
        for child in element_info.children():
            self.__generate_props_dict(child)
            child_item \
                = QStandardItem(self.__node_name(child))
            child_item.setEditable(False)
            parent.appendRow(child_item)
            self.__get_next(child, child_item)

    def __node_name(self, element_info):
        if 'uia' == self.backend:
            return '%s "%s" (%s)' % (str(element_info.control_type),
                                     str(element_info.name),
                                     id(element_info))
        return '"%s" (%s)' % (str(element_info.name), id(element_info))

    def __generate_props_dict(self, element_info):
        props = [
            ['control_id', str(element_info.control_id)],
            ['class_name', str(element_info.class_name)],
            ['enabled', str(element_info.enabled)],
            ['handle', str(element_info.handle)],
            ['name', str(element_info.name)],
            ['process_id', str(element_info.process_id)],
            ['rectangle', str(element_info.rectangle)],
            ['rich_text', str(element_info.rich_text)],
            ['visible', str(element_info.visible)]
        ]

        props_win32 = [
        ] if (self.backend == 'win32') else []

        props_uia = [
            ['auto_id', str(element_info.auto_id)],
            ['control_type', str(element_info.control_type)],
            ['element', str(element_info.element)],
            ['framework_id', str(element_info.framework_id)],
            ['runtime_id', str(element_info.runtime_id)],
            ['access_key', str(element_info.access_key)],
            ['legacy_action', str(element_info.legacy_action)],
            ['legacy_descr', str(element_info.legacy_descr)],
            ['legacy_help', str(element_info.legacy_help)],
            ['legacy_name', str(element_info.legacy_name)],
            ['legacy_shortcut', str(element_info.legacy_shortcut)],
            ['legacy_value', str(element_info.legacy_value)],
            ['accelerator', str(element_info.accelerator)],
            ['value', str(element_info.value)],
            ['parent', str(element_info.parent)],
            ['top_level_parent', str(element_info.top_level_parent)]
        ] if (self.backend == 'uia') else []

        props.extend(props_uia)
        props.extend(props_win32)
        node_dict = {self.__node_name(element_info): props}
        self.props_dict.update(node_dict)
        self.info_dict.update({self.__node_name(element_info): element_info})


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.header_labels = ['Property', 'Value']

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)


if __name__ == "__main__":
    main()
