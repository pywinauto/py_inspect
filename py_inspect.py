import pywinauto
from pywinauto import backend
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
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
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
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHeaderView
import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


class InfoDialog(QDialog):
    def __init__(self, title, items, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        listView = QListView()
        model = QStandardItemModel()
        listView.setModel(model)

        if type(items) == bool:
            model.appendRow(QStandardItem(str(items)))
        else:
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

        # vbox3.addStretch(1)
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
        if self.x.text() == '' and self.y.text() != '' or self.x.text() != '' and self.y.text() == '':
            QMessageBox.warning(self, "Attention",
                                "Please type coords correctly!")
        else:
            self.close()


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Methods
        self.base_methods = {
            # TODO remove overriden methods
            # 'capture_as_image': self.__capture_as_image,
            'children': self.__children,
            'click_input': self.__click_input,
            'close': self.__close,
            'descendants': self.__descendants,
            # 'draw_outline': self.__draw_outline,
            'set_focus': self.__set_focus,
            'texts': self.__texts,
            'type_keys': self.__type_keys,
            'wait_enabled': self.__wait_enabled,
            'wait_not_enabled': self.__wait_not_enabled,
            'wait_not_visible': self.__wait_not_visible,
            'wait_visible': self.__wait_visible,
            'window_text': self.__window_text
        }
        self.backend_methods = {
            'win32': {
                'backend_methods': {
                    'click': self.__win32_click,
                    'client_rect': self.__win32_client_rect,
                    'client_rects': self.__win32_client_rects,
                    'context_help_id': self.__win32_context_help_id,
                    'control_type': self.__win32_control_type,
                    'debug_message': self.__win32_debug_message,
                    'double_click': self.__win32_double_click,
                    'drag_mouse': self.__win32_drag_mouse,
                    'exstyle': self.__win32_exstyle,
                    'font': self.__win32_font,
                    'fonts': self.__win32_fonts,
                    'full_control_type': self.__win32_full_control_type,
                    'get_focus': self.__win32_get_focus,
                    'get_show_state': self.__win32_get_show_state,
                    'get_toolbar': self.__win32_get_toolbar,
                    'handle': self.__win32_handle,
                    'has_exstyle': self.__win32_has_exstyle,
                    'has_focus': self.__win32_has_focus,
                    'has_keyboard_focus': self.__win32_has_keyboard_focus,
                    'has_style': self.__win32_has_style,
                    'is_active': self.__win32_is_active,
                    'is_maximized': self.__win32_is_maximized,
                    'is_minimized': self.__win32_is_minimized,
                    'is_normal': self.__win32_is_normal,
                    'is_unicode': self.__win32_is_unicode,
                    'maximize': self.__win32_maximize,
                    'menu': self.__win32_menu,
                    'menu_item': self.__win32_menu_item,
                    'menu_items': self.__win32_menu_items,
                    'menu_select': self.__win32_menu_select,
                    'minimize': self.__win32_minimize,
                    'move_mouse': self.__win32_move_mouse,
                    'move_window': self.__win32_move_window,
                    'notify_parent': self.__win32_notify_parent,
                    'owner': self.__win32_owner,
                    'popup_window': self.__win32_popup_window,
                    'post_command': self.__win32_post_command,
                    'post_message': self.__win32_post_message,
                    'press_mouse': self.__win32_press_mouse,
                    'release_mouse': self.__win32_release_mouse,
                    'restore': self.__win32_restore,
                    'right_click': self.__win32_right_click,
                    'scroll': self.__win32_scroll,
                    'send_chars': self.__win32_send_chars,
                    'send_command': self.__win32_send_command,
                    'send_keystrokes': self.__win32_send_keystrokes,
                    'send_message': self.__win32_send_message,
                    'send_message_timeout': self.__win32_send_message_timeout,
                    'set_application_data': self.__win32_set_application_data,
                    'set_keyboard_focus': self.__win32_set_keyboard_focus,
                    'set_transparency': self.__win32_set_transparency,
                    'set_window_text': self.__win32_set_window_text,
                    'style': self.__win32_style,
                    'user_data': self.__win32_user_data
                },
                'controls_methods': {
                    'hwndwrapper.DialogWrapper': {'client_area_rect': None, 'force_close': None, 'show_in_taskbar': None, 'hide_from_taskbar': None, 'run_tests': None, 'write_to_xml': None, 'is_in_taskbar': None},
                    'win32_controls.ButtonWrapper': {'uncheck_by_click_input': None, 'uncheck_by_click': None, 'check_by_click_input': None, 'get_check_state': None, 'is_checked': None, 'uncheck': None, 'check': None, 'check_by_click': None, 'set_check_indeterminate': None},
                    'win32_controls.ComboBoxWrapper': {'selected_index': None, 'select': None, 'item_count': None, 'dropped_rect': None, 'item_data': None, 'selected_text': None, 'item_texts': None},
                    'win32_controls.ListBoxWrapper': {'set_item_focus': None, 'select': None, 'item_count': None, 'selected_indices': None, 'item_data': None, 'item_rect': None, 'item_texts': None, 'is_single_selection': None, 'get_item_focus': None},
                    'win32_controls.EditWrapper': {'get_line': None, 'select': None, 'line_length': None, 'selection_indices': None, 'line_count': None, 'set_text': None, 'text_block': None, 'set_edit_text': None},
                    'win32_controls.StaticWrapper': {},
                    'win32_controls.PopupMenuWrapper': {},
                    'common_controls.ListViewWrapper': {'items': None, 'get_header_control': None, 'columns': None, 'select': None, 'item_count': None, 'is_focused': None, 'get_column': None, 'get_item_rect': None, 'is_checked': None, 'uncheck': None, 'check': None, 'is_selected': None, 'get_selected_count': None, 'column_widths': None, 'column_count': None, 'item': None, 'get_item': None, 'deselect': None},
                    'common_controls.TreeViewWrapper': {'ensure_visible': None, 'select': None, 'print_items': None, 'item_count': None, 'is_selected': None, 'item': None, 'tree_root': None, 'get_item': None, 'roots': None},
                    'common_controls.HeaderWrapper': {'get_column_text': None, 'get_column_rectangle': None, 'item_count': None},
                    'common_controls.StatusBarWrapper': {'border_widths': None, 'get_part_text': None, 'get_part_rect': None, 'part_right_edges': None, 'part_count': None},
                    'common_controls.TabControlWrapper': {'row_count': None, 'get_tab_text': None, 'tab_count': None, 'get_tab_rect': None, 'select': None, 'get_selected_tab': None},
                    'common_controls.ToolbarWrapper': {'get_button': None, 'get_button_struct': None, 'check_button': None, 'press_button': None, 'get_tool_tips_control': None, 'tip_texts': None, 'get_button_rect': None, 'button': None, 'menu_bar_click_input': None, 'button_count': None},
                    'common_controls.ReBarWrapper': {'get_tool_tips_control': None, 'get_band': None, 'band_count': None},
                    'common_controls.ToolTipsWrapper': {'tool_count': None, 'get_tip': None, 'get_tip_text': None},
                    'common_controls.UpDownWrapper': {'decrement': None, 'set_base': None, 'increment': None, 'set_value': None, 'get_value': None, 'get_base': None, 'get_buddy_control': None, 'get_range': None},
                    'common_controls.TrackbarWrapper': {'set_range_min': None, 'get_line_size': None, 'set_position': None, 'set_line_size': None, 'get_sel_end': None, 'get_page_size': None, 'get_position': None, 'get_sel_start': None, 'set_page_size': None, 'get_num_ticks': None, 'get_tooltips_control': None, 'get_channel_rect': None, 'set_sel': None, 'get_range_min': None, 'get_range_max': None, 'set_range_max': None},
                    'common_controls.AnimationWrapper': {},
                    'common_controls.ComboBoxExWrapper': {},
                    'common_controls.DateTimePickerWrapper': {'set_time': None, 'get_time': None},
                    'common_controls.HotkeyWrapper': {},
                    'common_controls.IPAddressWrapper': {},
                    'common_controls.CalendarWrapper': {'get_view': None, 'set_today': None, 'get_id': None, 'set_current_date': None, 'set_border': None, 'get_today': None, 'get_current_date': None, 'set_day_states': None, 'hit_test': None, 'set_first_weekday': None, 'set_id': None, 'get_month_range': None, 'set_color': None, 'set_view': None, 'calc_min_rectangle': None, 'get_border': None, 'set_month_delta': None, 'place_in_calendar': None, 'get_month_delta': None, 'count': None, 'get_first_weekday': None},
                    'common_controls.PagerWrapper': {'set_position': None, 'get_position': None},
                    'common_controls.ProgressWrapper': {'set_position': None, 'get_step': None, 'step_it': None, 'get_state': None, 'get_position': None}
                }
            },
            'uia': {
                'backend_methods': {
                    'can_select_multiple': self.__uia_can_select_multiple,
                    'children_texts': self.__uia_children_texts,
                    'collapse': self.__uia_collapse,
                    'expand': self.__uia_expand,
                    'get_expand_state': self.__uia_get_expand_state,
                    'get_selection': self.__uia_get_selection,
                    'get_show_state': self.__uia_get_show_state,
                    'has_keyboard_focus': self.__uia_has_keyboard_focus,
                    'invoke': self.__uia_invoke,
                    'is_active': self.__uia_is_active,
                    'is_collapsed': self.__uia_is_collapsed,
                    'is_expanded': self.__uia_is_expanded,
                    'is_keyboard_focusable': self.__uia_is_keyboard_focusable,
                    'is_maximized': self.__uia_is_maximized,
                    'is_minimized': self.__uia_is_minimized,
                    'is_normal': self.__uia_is_normal,
                    'is_selected': self.__uia_is_selected,
                    'is_selection_required': self.__uia_is_selection_required,
                    'legacy_properties': self.__uia_legacy_properties,
                    'maximize': self.__uia_maximize,
                    'menu_select': self.__uia_menu_select,
                    'minimize': self.__uia_minimize,
                    'move_window': self.__uia_move_window,
                    'restore': self.__uia_restore,
                    'scroll': self.__uia_scroll,
                    'select': self.__uia_select,
                    'selected_item_index': self.__uia_selected_item_index,
                    'set_value': self.__uia_set_value
                },
                'controls_methods': {
                    'uia_controls.WindowWrapper': {},
                    'uia_controls.ButtonWrapper': {'get_toggle_state': None, 'toggle': None, 'click': None},
                    'uia_controls.ComboBoxWrapper': {'item_count': None, 'selected_index': None, 'is_editable': None, 'selected_text': None},
                    'uia_controls.EditWrapper': {'selection_indices': None, 'set_edit_text': None, 'set_window_text': None, 'is_editable': None, 'get_value': None, 'line_count': None, 'set_text': None, 'text_block': None, 'line_length': None, 'get_line': None},
                    'uia_controls.TabControlWrapper': {'tab_count': None, 'get_selected_tab': None},
                    'uia_controls.SliderWrapper': {'small_change': None, 'value': None, 'min_value': None, 'max_value': None, 'large_change': None},
                    'uia_controls.HeaderWrapper': {},
                    'uia_controls.HeaderItemWrapper': {},
                    'uia_controls.ListItemWrapper': {'is_checked': None},
                    'uia_controls.ListViewWrapper': {'item_count': None, 'columns': None, 'items': None, 'get_column': None, 'get_header_controls': None, 'get_items': None, 'get_header_control': None, 'cell': None, 'item': None, 'get_item': None, 'column_count': None, 'cells': None, 'get_item_rect': None, 'get_selected_count': None},
                    'uia_controls.MenuItemWrapper': {'items': None},
                    'uia_controls.MenuWrapper': {'item_by_path': None, 'items': None, 'item_by_index': None},
                    'uia_controls.TooltipWrapper': {},
                    'uia_controls.ToolbarWrapper': {'button': None, 'button_count': None, 'buttons': None, 'check_button': None},
                    'uia_controls.TreeItemWrapper': {'get_child': None, 'is_checked': None, 'ensure_visible': None, 'sub_elements': None},
                    'uia_controls.TreeViewWrapper': {'item_count': None, 'get_item': None, 'roots': None, 'print_items': None},
                    'uia_controls.StaticWrapper': {}
                }
            },
            'ax': {
                'backend_methods': {
                },
                'controls_methods': {
                }
            },
            # TODO HOW TO ADD BACKEND
            'other backend': {
                'backend_methods': {
                    'other backend method 1': 'self.implementing_function_name',
                    'other backend method 2': 'self.implementing_function_name',
                },
                'controls_methods': {
                    'other backend control wrapper 1': {'unique method 1': 'self.implementing_function_name', 'unique method 2': 'self.implementing_function_name'},
                    'other backend control wrapper 2': {'unique method 1': 'self.implementing_function_name', 'unique method 2': 'self.implementing_function_name'}
                }
            }
        }

        # TODO try resize instead
        self.setMinimumSize(1024, 768)
        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.setWindowTitle(
            QCoreApplication.translate("MainWindow", "PyInspect"))

        self.settings = QSettings('py_inspect', 'MainWindow')

        self.current_elem_wrapper = None

        # Main layout
        self.mainLayout = QVBoxLayout()

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.action = self.menu_bar.addMenu("Actions")
        self.mouse = QAction('Find by mouse', self)
        self.mouse.setCheckable(True)
        default = QAction('Default Action', self)
        default.triggered.connect(self.__default)
        self.action.addAction(self.mouse)
        self.action.addAction(default)
        self.action.addSeparator()

        self.bmethods = self.action.addMenu("Base Wrapper Methods")

        self.hmethods = self.action.addMenu("Hwnd Wrapper Methods")
        self.hmethods.menuAction().setVisible(False)
        self.umethods = self.action.addMenu("UIA Wrapper Methods")
        self.umethods.menuAction().setVisible(False)
        self.amethods = self.action.addMenu("AX Wrapper Methods")
        self.amethods.menuAction().setVisible(False)
        self.backend_menus = {
            'last_used': self.umethods,
            'win32': self.hmethods,
            'uia': self.umethods,
            'ax': self.amethods,
            # TODO HOW TO ADD BACKEND
            'other backend': 'self.other_backend_menu'
        }

        self.cmethods = self.action.addMenu('Current Wrapper Unique Methods')
        self.backend_wrappers = {
            'win32': 'hwndwrapper.HwndWrapper',
            'uia': 'uiawrapper.UIAWrapper',
            # TODO macos support
            'ax': '',
            # TODO HOW TO ADD BACKEND
            'other backend': 'other backend wrapper name'
        }
        self.backend_inits = {
            'win32': pywinauto.controls.hwndwrapper.HwndWrapper,
            'uia': pywinauto.controls.uiawrapper.UIAWrapper,
            # TODO macos support
            'ax': None,
            # TODO HOW TO ADD BACKEND
            'other backend': 'other backend wrapper class name'
        }

        # Backend label
        self.backendLabel = QLabel("Backend Type")

        # Backend combobox
        self.comboBox = QComboBox()
        self.comboBox.setMouseTracking(False)
        self.comboBox.setMaxVisibleItems(5)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated[str].connect(self.__show_tree)

        # Refresh button
        self.refresh = QPushButton('Refresh')
        self.refresh.clicked.connect(self.__refresh)

        # Tree view
        self.tree_view = QTreeView()
        self.tree_view.setColumnWidth(0, 150)
        self.tree_view.clicked.connect(self.__show_property)

        if sys.platform == 'darwin':
            self.comboBox.addItem('ax')
            self.__initialize_calc('ax')
        else:
            for _backend in backend.registry.backends.keys():
                self.comboBox.addItem(_backend)
            self.comboBox.setCurrentText('uia')
            self.__initialize_calc()

        # Code generator
        self.editLabel = QLabel('Code generator')
        self.script_mode = QComboBox()
        self.script_mode.addItem('connect to app mode')
        self.script_mode.addItem('start .exe mode')
        self.clear = QPushButton('Clear')
        self.clear.clicked.connect(self.__clear_edit)
        self.save = QPushButton('Save to file')
        self.save.clicked.connect(self.__save_edit)
        self.edit = QTextEdit()
        self.used_apps = {}
        self.flags = 0

        # Table view
        self.table_view = QTableView()

        # Add top widgets to main window
        self.grid_tree = QGridLayout()
        self.grid_tree.addWidget(self.backendLabel, 0, 0, 1, 1)
        self.grid_tree.addWidget(self.comboBox, 0, 1, 1, 1)
        self.grid_tree.addWidget(self.refresh, 0, 2, 1, 1)
        self.grid_tree.addWidget(self.tree_view, 1, 0, 1, 3)
        self.tree = QGroupBox('Controls View')
        self.tree.setLayout(self.grid_tree)

        self.grid_table = QGridLayout()
        self.grid_table.addWidget(self.editLabel, 0, 0, 1, 1)
        self.grid_table.addWidget(self.script_mode, 0, 1, 1, 1)
        self.grid_table.addWidget(self.clear, 0, 2, 1, 1)
        self.grid_table.addWidget(self.save, 0, 3, 1, 1)
        self.grid_table.addWidget(self.edit, 1, 0, 1, 4)
        self.grid_table.addWidget(self.table_view, 2, 0, 1, 4)
        self.table = QGroupBox('Properties View')
        self.table.setLayout(self.grid_table)

        self.mainLayout.addWidget(self.menu_bar)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.tree)
        self.hbox.addWidget(self.table)
        self.mainLayout.addLayout(self.hbox)
        self.setLayout(self.mainLayout)
        geometry = self.settings.value('Geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)

    def __initialize_calc(self, _backend='uia'):
        self.element_info \
            = backend.registry.backends[_backend].element_info_class()
        self.tree_model = MyTreeModel(self.element_info, _backend)
        self.tree_model.setHeaderData(0, Qt.Horizontal, 'Controls')
        self.tree_view.setModel(self.tree_model)

    def __show_tree(self, text):
        backend = text
        if str(self.comboBox.currentText()) != backend:
            self.current_elem_wrapper = None
            self.__initialize_calc(backend)

    def __show_property(self, index=None):
        data = index.data()
        current_backend = self.comboBox.currentText()
        self.current_elem_info = self.tree_model.info_dict.get(data)
        self.current_elem_wrapper = self.backend_inits[current_backend](
            self.current_elem_info)

        self.bmethods.clear()
        for method in self.base_methods.keys():
            action = QAction(method + '()', self)
            action.triggered.connect(self.base_methods[method])
            self.bmethods.addAction(action)

        self.backend_menus['last_used'].menuAction().setVisible(False)
        self.backend_menus['last_used'] = self.backend_menus[current_backend]
        self.backend_menus[current_backend].clear()
        self.backend_menus[current_backend].menuAction().setVisible(True)
        for method in self.backend_methods[current_backend]['backend_methods'].keys():
            # if while not all implemented
            if self.backend_methods[current_backend]['backend_methods'][method] is not None:
                action = QAction(method + '()', self)
                action.triggered.connect(
                    self.backend_methods[current_backend]['backend_methods'][method])
                self.backend_menus[current_backend].addAction(action)

        wrapper = str(self.current_elem_wrapper).split('-')[0][:-1]
        if wrapper != self.backend_wrappers[current_backend]:
            self.cmethods.clear()
            if wrapper in self.backend_methods[current_backend]['controls_methods'].keys():
                for method in self.backend_methods[current_backend]['controls_methods'][wrapper].keys():
                    # if while not all implemented
                    if self.backend_methods[current_backend]['controls_methods'][wrapper][method] is not None:
                        action = QAction(method + '()', self)
                        action.triggered.connect(
                            self.backend_methods[current_backend]['controls_methods'][wrapper][method])
                        self.cmethods.addAction(action)
            else:
                dlg = InfoDialog('Not implemented yet',
                                 'Unknown wrapper: ' + wrapper, self)
                dlg.exec()

        self.table_model \
            = MyTableModel(self.tree_model.props_dict.get(data), self)
        self.table_view.wordWrap()
        self.table_view.setModel(self.table_model)
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def __refresh(self):
        self.current_elem_wrapper = None
        self.tree_model = MyTreeModel(
            self.element_info, str(self.comboBox.currentText()))
        self.tree_model.setHeaderData(0, Qt.Horizontal, 'Controls')
        self.tree_view.setModel(self.tree_model)

    def __clear_edit(self):
        self.edit.clear()
        self.used_apps = {}
        self.flags = 0

    def __save_edit(self):
        save_file = QFileDialog.getSaveFileName(
            None, 'SaveTextFile', '/', "Python Script (*.py)")
        text = self.edit.toPlainText()
        if save_file[0]:
            with open(save_file[0], 'w', encoding='utf8') as file:
                file.write(text)

    def __write_method(self, method, ret):
        if len(self.used_apps) == 0:
            self.edit.append('from pywinauto.application import Application\n')
        top_parent = self.current_elem_info.top_level_parent
        elem_info = self.current_elem_info
        path = [elem_info]
        if top_parent != elem_info:
            while elem_info.parent != top_parent:
                path.append(elem_info.parent)
                elem_info = elem_info.parent

        # check if already used
        if top_parent.process_id not in self.used_apps.keys():
            self.used_apps[top_parent.process_id] = 'app_{}'.format(
                len(self.used_apps) + 1)
            if self.script_mode.currentText() == 'connect to app mode':
                args = ''
                if top_parent.process_id:
                    args = 'pid=' + str(top_parent.process_id)
                elif top_parent.handle:
                    args = 'handle=' + str(top_parent.handle)
                else:
                    # TODO same as start mode
                    args = 'cannot find app'
                self.edit.append(self.used_apps[top_parent.process_id] +
                                 ' = Application(backend="{}").connect({})\n'.format(self.comboBox.currentText(), args))
            elif self.script_mode.currentText() == 'start .exe mode':
                # TODO start correct app name
                self.edit.append(self.used_apps[top_parent.process_id] + ' = Application(backend="{}").start("{}")\n'.format(
                    self.comboBox.currentText(), 'type correct argument for start()'))
        command = str(self.used_apps[top_parent.process_id])
        # TODO try optimal search for controls with pre-run script
        window = path[len(path)-1]
        path = path[:-1]
        window_props = ''
        if window.name:
            window_props += 'name="{}", '.format(window.name)
        if window.class_name:
            window_props += 'class_name="{}", '.format(window.class_name)
        if window.control_id:
            window_props += 'control_id="{}", '.format(window.control_id)
        if window_props == '':
            if self.comboBox.currentText() == 'uia':
                if window.control_type:
                    window_props += 'control_type="{}", '.format(
                        window.control_type)
                if window.auto_id:
                    window_props += 'auto_id="{}", '.format(window.auto_id)
                if window_props == '':
                    window_props = 'cannot find window by name, class_name, control_id, control_type or auto_id, try other props'
                else:
                    window_props = window_props[:-2]
            else:
                window_props = 'cannot find control by name, class_name or control_id, try other props'
        else:
            window_props = window_props[:-2]
        command += '.window({}, top_level_only=False)'.format(window_props)
        for ctrl in path[::-1]:
            ctrl_props = ''
            if ctrl.name:
                ctrl_props += 'name="{}", '.format(ctrl.name)
            if ctrl.class_name:
                ctrl_props += 'class_name="{}", '.format(ctrl.class_name)
            if ctrl.control_id:
                ctrl_props += 'control_id="{}", '.format(ctrl.control_id)
            if ctrl_props == '':
                if self.comboBox.currentText() == 'uia':
                    if ctrl.control_type:
                        ctrl_props += 'control_type="{}", '.format(
                            ctrl.control_type)
                    if ctrl.auto_id:
                        ctrl_props += 'auto_id="{}", '.format(ctrl.auto_id)
                    if ctrl_props == '':
                        ctrl_props = 'cannot find control by name, class_name, control_id, control_type or auto_id, try other props'
                    else:
                        ctrl_props = ctrl_props[:-2]
                else:
                    ctrl_props = 'cannot find control by name, class_name or control_id, try other props'
            else:
                ctrl_props = ctrl_props[:-2]
            command += '.by({})'.format(ctrl_props)
        command += '.' + method
        if ret == 'execute':
            self.edit.append(command + '\n')
        elif ret == 'print':
            self.edit.append('print({})\n'.format(command))
        elif ret == 'check':
            self.edit.append('flag_{} = {}\n'.format(self.flags, command))
            self.flags += 1

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('Geometry', geometry)
        super(MyWindow, self).closeEvent(event)

    # Actions

    def __default(self):
        # TODO add write method?
        if self.comboBox.currentText() == 'uia':
            if self.current_elem_info.legacy_action != '':
                self.current_elem_wrapper.iface_legacy_iaccessible.DoDefaultAction()
            else:
                self.current_elem_wrapper.set_focus()
        else:
            # TODO find default action in other backends
            pass

    # Base Wrapper Methods

    # def __capture_as_image(self):
    #    img = self.current_elem_wrapper.capture_as_image()
    #    if img != None:
    #        img.show()
    #    else:
    #        print('can not capture as image')

    def __children(self):
        dlg = InfoDialog(
            'children()', self.current_elem_wrapper.children(), self)
        dlg.exec()
        self.__write_method('children()', 'print')

    # TODO there are more arguments in actual click_input
    def __click_input(self):
        dlg = ClickInput(self)
        dlg.exec()
        button = 'left'
        coords = (None, None)
        double = False
        wheel_dist = 0
        if dlg.right.isChecked():
            button = 'right'
        elif dlg.middle.isChecked():
            button = 'middle'
        if dlg.x.text() != '':
            coords = (int(dlg.x.text()), int(dlg.y.text()))
        if dlg.double.isChecked():
            double = True
        if dlg.wheel_dist.text() != '':
            wheel_dist = int(dlg.wheel_dist.text())
        self.__write_method('click_input(button=' + button + ', coords=' + str(coords) +
                            ', double=' + str(double) + ', wheel_dist=' + str(wheel_dist) + ')', 'execute')
        self.current_elem_wrapper.click_input(
            button=button, coords=coords, double=double, wheel_dist=wheel_dist)

    def __close(self):
        if self.current_elem_wrapper:
            if self.current_elem_wrapper.is_dialog():
                self.__write_method('close()', 'execute')
                self.current_elem_wrapper.close()
                self.__refresh()
            else:
                dlg = InfoDialog(
                    'close()', ['control <<' + str(self.current_elem_wrapper) + '>> is not a window'], self)
                dlg.exec()

    def __descendants(self):
        dlg = InfoDialog(
            'descendants()', self.current_elem_wrapper.descendants(), self)
        dlg.exec()
        self.__write_method('descendants()', 'print')

    # def __draw_outline(self):
    #    self.current_elem_wrapper.draw_outline()

    def __set_focus(self):
        self.__write_method('set_focus()', 'execute')
        self.current_elem_wrapper.set_focus()

    def __texts(self):
        dlg = InfoDialog('texts()', self.current_elem_wrapper.texts(), self)
        dlg.exec()
        self.__write_method('texts()', 'print')

    def __type_keys(self):
        # TODO show dialog to choose keys + write method
        # self.current_elem_wrapper.type_keys()
        pass

    def __wait_enabled(self):
        self.__write_method('wait_enabled()', 'execute')
        self.current_elem_wrapper.wait_enabled()

    def __wait_not_enabled(self):
        self.__write_method('wait_not_enabled()', 'execute')
        self.current_elem_wrapper.wait_not_enabled()

    def __wait_not_visible(self):
        self.__write_method('wait_not_visible()', 'execute')
        self.current_elem_wrapper.wait_not_visible()

    def __wait_visible(self):
        self.__write_method('wait_visible()', 'execute')
        self.current_elem_wrapper.wait_visible()

    def __window_text(self):
        dlg = InfoDialog(
            'window_text', [self.current_elem_wrapper.window_text()], self)
        dlg.exec()
        self.__write_method('window_text()', 'print')

    # Hwnd Wrapper Methods

    def __win32_click(self):
        pass

    def __win32_click(self):
        pass

    def __win32_client_rect(self):
        pass

    def __win32_client_rects(self):
        pass

    def __win32_context_help_id(self):
        pass

    def __win32_control_type(self):
        pass

    def __win32_debug_message(self):
        pass

    def __win32_double_click(self):
        pass

    def __win32_drag_mouse(self):
        pass

    def __win32_exstyle(self):
        pass

    def __win32_font(self):
        pass

    def __win32_fonts(self):
        pass

    def __win32_full_control_type(self):
        pass

    def __win32_get_focus(self):
        pass

    def __win32_get_show_state(self):
        pass

    def __win32_get_toolbar(self):
        pass

    def __win32_handle(self):
        pass

    def __win32_has_exstyle(self):
        pass

    def __win32_has_focus(self):
        pass

    def __win32_has_keyboard_focus(self):
        pass

    def __win32_has_style(self):
        pass

    def __win32_is_active(self):
        pass

    def __win32_is_maximized(self):
        pass

    def __win32_is_minimized(self):
        pass

    def __win32_is_normal(self):
        pass

    def __win32_is_unicode(self):
        pass

    def __win32_maximize(self):
        pass

    def __win32_menu(self):
        pass

    def __win32_menu_item(self):
        pass

    def __win32_menu_items(self):
        pass

    def __win32_menu_select(self):
        pass

    def __win32_minimize(self):
        pass

    def __win32_move_mouse(self):
        pass

    def __win32_move_window(self):
        pass

    def __win32_notify_parent(self):
        pass

    def __win32_owner(self):
        pass

    def __win32_popup_window(self):
        pass

    def __win32_post_command(self):
        pass

    def __win32_post_message(self):
        pass

    def __win32_press_mouse(self):
        pass

    def __win32_release_mouse(self):
        pass

    def __win32_restore(self):
        pass

    def __win32_right_click(self):
        pass

    def __win32_scroll(self):
        pass

    def __win32_send_chars(self):
        pass

    def __win32_send_command(self):
        pass

    def __win32_send_keystrokes(self):
        pass

    def __win32_send_message(self):
        pass

    def __win32_send_message_timeout(self):
        pass

    def __win32_set_application_data(self):
        pass

    def __win32_set_keyboard_focus(self):
        pass

    def __win32_set_transparency(self):
        pass

    def __win32_set_window_text(self):
        pass

    def __win32_style(self):
        pass

    def __win32_user_data(self):
        pass

    # Hwnd Controls Wrappers Methods

    # UIA Wrapper Methods

    def __uia_can_select_multiple(self):
        pass

    def __uia_children_texts(self):
        pass

    def __uia_collapse(self):
        pass

    def __uia_expand(self):
        pass

    def __uia_get_expand_state(self):
        pass

    def __uia_get_selection(self):
        pass

    def __uia_get_show_state(self):
        pass

    def __uia_has_keyboard_focus(self):
        pass

    def __uia_invoke(self):
        pass

    def __uia_is_active(self):
        pass

    def __uia_is_collapsed(self):
        pass

    def __uia_is_expanded(self):
        pass

    def __uia_is_keyboard_focusable(self):
        pass

    def __uia_is_maximized(self):
        pass

    def __uia_is_minimized(self):
        pass

    def __uia_is_normal(self):
        pass

    def __uia_is_selected(self):
        pass

    def __uia_is_selection_required(self):
        pass

    def __uia_legacy_properties(self):
        pass

    def __uia_maximize(self):
        pass

    def __uia_menu_select(self):
        pass

    def __uia_minimize(self):
        pass

    def __uia_move_window(self):
        pass

    def __uia_restore(self):
        pass

    def __uia_scroll(self):
        pass

    def __uia_select(self):
        pass

    def __uia_selected_item_index(self):
        pass

    def __uia_set_value(self):
        pass

    # UIA Controls Wrappers Methods

    # AX Wrapper Methods

    # AX Controls Wrappers Methods


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
            ['name', str(element_info.name)],
            ['process_id', str(element_info.process_id)],
            ['rectangle', str(element_info.rectangle)],
            ['rich_text', str(element_info.rich_text)],
            ['visible', str(element_info.visible)]
        ] if (self.backend == 'ax') else [
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
