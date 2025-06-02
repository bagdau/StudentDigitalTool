import sys
import os
import json
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import subprocess
import signal


import atexit

try:
    from PIL import Image
except ImportError:
    Image = None  # Если Pillow не установлен
    

# === Локализация ===
LANGS = ['EN', 'KZ', 'RU']
TRANSLATIONS = {
    'EN': {
        'title': 'SmartUkgu Desktop',
        'main': 'Home',
        'schedule': 'Schedule',
        'news': 'News',
        'chatgpt': 'ChatGPT',
        'account': 'Account',
        'save': 'Save Data',
        'calculator': 'Calculator',
        'file': 'File',
        'edit': 'Edit',
        'copy': 'Copy',
        'paste': 'Paste',
        'tools': 'Tools',
        'help': 'Help',
        'view': 'View',
        'google': 'Lets Google it!',
        'google_search': 'Google Search...',
        'about': 'About',
        'close': 'Close',
        'autofill': 'Enable autofill',
        'modal_title': 'Your login data',
        'login': 'Login',
        'iin': 'IIN',
        'password': 'Password',
        'success': 'Data saved successfully.',
        'manual_save': 'Save Data',
        'search_prompt': 'What to search?',
        'search_title': 'Google Search',
        'ok': 'OK',
        'cancel': 'Cancel'
    },
    'KZ': {
        'title': 'SmartUkgu веб - қосымшасы',
        'main': 'Басты бет',
        'schedule': 'Кесте',
        'news': 'Жаңалықтар',
        'chatgpt': 'ChatGPT',
        'account': 'Аккаунт',
        'save': 'Деректерді сақтау',
        'calculator': 'Калькулятор',
        'file': 'Файл',
        'edit': 'Өңдеу',
        'copy': 'Көшіру',
        'paste': 'Қою',
        'tools': 'Құралдар',
        'help': 'Анықтама',
        'view': 'Көрініс',
        'google': 'Гуглить ету',
        'google_search': 'Google іздеу...',
        'about': 'Жоба туралы',
        'close': 'Жабу',
        'autofill': 'Авто-толтыруды қосу',
        'modal_title': 'Кіру деректері',
        'login': 'Логин',
        'iin': 'ЖСН',
        'password': 'Құпиясөз',
        'success': 'Деректер сәтті сақталды.',
        'manual_save': 'Деректерді сақтау',
        'search_prompt': 'Не іздейміз?',
        'search_title': 'Google іздеу',
        'ok': 'OK',
        'cancel': 'Болдырмау'
    },
    'RU': {
        'title': 'SmartUkgu веб-приложение',
        'main': 'Главная',
        'schedule': 'Расписание',
        'news': 'Новости',
        'chatgpt': 'ChatGPT',
        'account': 'Аккаунт',
        'save': 'Сохранить данные',
        'calculator': 'Калькулятор',
        'file': 'Файл',
        'edit': 'Правка',
        'copy': 'Копировать',
        'paste': 'Вставить', 
        'tools': 'Инструменты',
        'help': 'Справка',
        'view': 'Вид',
        'google': 'Давай погуглим!',
        'google_search': 'Поиск в Google...',
        'about': 'О программе',
        'close': 'Закрыть',
        'autofill': 'Включить авто-заполнение',
        'modal_title': 'Ваши данные для входа',
        'login': 'Логин',
        'iin': 'ИИН',
        'password': 'Пароль',
        'success': 'Данные успешно сохранены.',
        'manual_save': 'Сохранить данные',
        'search_prompt': 'Что ищем?',
        'search_title': 'Google Поиск',
        'ok': 'OK',
        'cancel': 'Отмена'
    }
}

def resource_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.abspath(rel_path)


ICONS_PATH = Path(resource_path("smartukgu-desktop/src/icons"))
DATA_FILE = Path(resource_path("smartukgu-desktop/src/data/account_info.json"))
SERVER_SCRIPT = Path(resource_path("smartukgu-desktop/src/save_server.py"))


print("ICONS_PATH", ICONS_PATH)
print("DATA_FILE", DATA_FILE)
print("SERVER_SCRIPT", SERVER_SCRIPT)

if hasattr(sys, '_MEIPASS'):
    server_path = os.path.join(sys._MEIPASS, 'save_server.py')
else:
    server_path = os.path.abspath('save_server.py')



def ensure_icon():
    icon_src = ICONS_PATH / "logo.png"
    icon_out = ICONS_PATH / "UKGULogotype.png"
    ico_out = ICONS_PATH / "main.ico"
    if not icon_out.exists():
        if Image:
            img = Image.open(icon_src)
            img.save(icon_out, format='PNG')
            img.save(ico_out, format='ICO')
        else:
            print("Pillow is not installed, cannot create icons.")


ensure_icon()

def handle_sigint(signum, frame):
    QtWidgets.QApplication.quit()

signal.signal(signal.SIGINT, handle_sigint)
def load_account_info():
    if DATA_FILE.exists():
        with DATA_FILE.open('r', encoding='utf-8') as f:
            return json.load(f)
    return {'login': '', 'password': '', 'iin': ''}

def save_account_info(login, password):
    info = {'login': login, 'password': password}
    if len(login) == 12 and login.isdigit():
        info['iin'] = login
    else:
        info['iin'] = ''
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    return info

def start_local_server():
    if not SERVER_SCRIPT.exists():
        QtWidgets.QMessageBox.critical(None, "Ошибка запуска сервера",
                                       f"Файл сервера не найден:\n{SERVER_SCRIPT.resolve()}")
        return None
    # Стартуем сервер в фоне на 127.0.0.1:5000 (Flask по умолчанию)
    if os.name == "nt":
        proc = subprocess.Popen([sys.executable, str(SERVER_SCRIPT)],
                                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        proc = subprocess.Popen([sys.executable, str(SERVER_SCRIPT)])
    return proc

def kill_server_on_exit(proc):
    def _kill():
        if proc:
            try:
                proc.terminate()
            except Exception:
                pass
    atexit.register(_kill)

class SmartUkguMain(QtWidgets.QMainWindow):
    def __init__(self, server_proc=None):
        super().__init__()
        self.lang = 'RU'
        self.setWindowTitle(self.trn('SmartUkgu Desktop'))
        self.setStyleSheet("QMainWindow { background-color: #f0f0f0; }")
        self.setMinimumSize(900, 700)
        self.setMaximumSize(1600, 1200)
        self.setGeometry(150, 90, 1100, 750)
        self.setWindowIcon(QtGui.QIcon(str(ICONS_PATH / "UKGULogotype.png")))
        self.account_info = load_account_info()
        self.autofill_enabled = False
        self.server_proc = server_proc

        self.web = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.web)
        self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru"))

        self.toolbar = QtWidgets.QToolBar("Навигация")
        self.toolbar.setIconSize(QtCore.QSize(26,26))
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self._add_toolbar_buttons()
        self._add_menu()

        self.web.loadFinished.connect(self.inject_js)

    def trn(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    def _add_toolbar_buttons(self):
        self.toolbar.clear()
        def add_toolbar_action(icon, key, func):
            action = QtWidgets.QAction(QtGui.QIcon(str(ICONS_PATH / icon)), self.trn(key), self)
            action.triggered.connect(func)
            self.toolbar.addAction(action)
        add_toolbar_action("main.png", "main", lambda: self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru")))
        add_toolbar_action("schedule.png", "schedule", lambda: self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru/undergraduate/academic-calendar")))
        add_toolbar_action("news.png", "news", lambda: self.web.setUrl(QtCore.QUrl("https://news.google.com/")))
        add_toolbar_action("chatgpt.png", "chatgpt", lambda: self.web.setUrl(QtCore.QUrl("ChatGPT.exe")))
        self.toolbar.addSeparator()
        add_toolbar_action("account.png", "account", self.show_account_modal)
        add_toolbar_action("savedata.png", "manual_save", self.manual_save_dialog)
        add_toolbar_action("calculator.png", "calculator", lambda: self.web.setUrl(QtCore.QUrl("https://www.google.com/search?q=калькулятор")))
        self.toolbar.addSeparator()
        # Language switcher
        lang_btn = QtWidgets.QToolButton(self)
        lang_btn.setText(self.lang)
        lang_btn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        lang_menu = QtWidgets.QMenu(self)
        for lng in LANGS:
            lang_menu.addAction(lng, lambda l=lng: self.set_language(l))
        lang_btn.setMenu(lang_menu)
        self.toolbar.addWidget(lang_btn)

    def _add_menu(self):
        menubar = self.menuBar()
        menubar.clear()
        file_menu = menubar.addMenu(self.trn("file"))
        file_menu.addAction(self.trn("main"), lambda: self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru")))
        file_menu.addAction(self.trn("schedule"), lambda: self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru/schedule")))
        file_menu.addSeparator()
        file_menu.addAction(self.trn("close"), self.close)

        edit_menu = menubar.addMenu(self.trn("edit"))
        edit_menu.addAction("Копировать", lambda: self.web.triggerPageAction(QtWebEngineWidgets.QWebEnginePage.Copy))
        edit_menu.addAction("Вставить", lambda: self.web.triggerPageAction(QtWebEngineWidgets.QWebEnginePage.Paste))

        tools_menu = menubar.addMenu(self.trn("tools"))
        tools_menu.addAction(self.trn("chatgpt"), lambda: self.web.setUrl(QtCore.QUrl("https://chat.openai.com/")))
        tools_menu.addAction(self.trn("calculator"), lambda: self.web.setUrl(QtCore.QUrl("https://www.google.com/search?q=калькулятор")))
        tools_menu.addAction(self.trn("news"), lambda: self.web.setUrl(QtCore.QUrl("https://news.google.com/")))
        tools_menu.addAction("PhotoMath", lambda: self.web.setUrl(QtCore.QUrl("https://photomath.com/")))

        acc_menu = menubar.addMenu(self.trn("account"))
        acc_menu.addAction(self.trn("modal_title"), self.show_account_modal)
        acc_menu.addAction(self.trn("autofill"), self.enable_autofill)
        acc_menu.addAction(self.trn("manual_save"), self.manual_save_dialog)

        help_menu = menubar.addMenu(self.trn("help"))
        help_menu.addAction(self.trn("about"), lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://smart.ukgu.kz/ru/about")))
        help_menu.addAction(self.trn("help"), lambda: self.web.setUrl(QtCore.QUrl("https://smart.ukgu.kz/ru/help")))

        view_menu = menubar.addMenu(self.trn("view"))
        view_menu.addAction("Стандартный", lambda: self.resize(900, 700))
        view_menu.addAction("Большой", lambda: self.resize(1200, 900))

        google_menu = menubar.addMenu(self.trn("google"))
        google_menu.addAction(self.trn("google"), self.open_google)
        google_menu.addAction(self.trn("google_search"), self.google_search_dialog)

    

    def set_language(self, lang):
        self.lang = lang
        self.setWindowTitle(self.trn('title'))
        self._add_toolbar_buttons()
        self._add_menu()

    def inject_js(self):
        if self.autofill_enabled and self.account_info.get("login"):
            login = self.account_info.get("login", "")
            password = self.account_info.get("password", "")
            fill_js = f"""
                let form = document.querySelector('form[action*="/login"]');
                if (form) {{
                    let l = form.querySelector('input[name="login"]');
                    let p = form.querySelector('input[name="password"]');
                    if(l) l.value = `{login}`;
                    if(p) p.value = `{password}`;
                }}
            """
            self.web.page().runJavaScript(fill_js)

    def show_account_modal(self):
        acc = self.account_info
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(self.trn("modal_title"))
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(
            f"<b>{self.trn('login')}:</b> {acc.get('login','')}<br>"
            f"<b>{self.trn('iin')}:</b> {acc.get('iin','')}<br>"
            f"<b>{self.trn('password')}:</b> {acc.get('password','')}"
        )
        msg.addButton(self.trn("close"), QtWidgets.QMessageBox.AcceptRole)
        msg.exec_()

    def enable_autofill(self):
        self.autofill_enabled = True
        self.inject_js()
        QtWidgets.QMessageBox.information(self, self.trn("autofill"), self.trn("autofill") + " ON")

    def manual_save_dialog(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle(self.trn("manual_save"))
        dlg.setModal(True)
        layout = QtWidgets.QFormLayout(dlg)
        login_edit = QtWidgets.QLineEdit()
        password_edit = QtWidgets.QLineEdit()
        password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addRow(self.trn("login"), login_edit)
        layout.addRow(self.trn("password"), password_edit)
        btn = QtWidgets.QPushButton(self.trn("save"))
        layout.addRow(btn)
        def save_and_close():
            login = login_edit.text().strip()
            password = password_edit.text().strip()
            info = save_account_info(login, password)
            self.account_info = info
            QtWidgets.QMessageBox.information(self, self.trn("success"), self.trn("success"))
            dlg.accept()
        btn.clicked.connect(save_and_close)
        dlg.exec_()



    def open_google(self):
        self.web.setUrl(QtCore.QUrl("https://www.google.com/"))

    def google_search_dialog(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, self.trn("search_title"), self.trn("search_prompt"))
        if ok and text.strip():
            url = "https://www.google.com/search?q=" + QtCore.QUrl.toPercentEncoding(text)
            self.web.setUrl(QtCore.QUrl(url))

    def closeEvent(self, event):
        if self.server_proc:
            try:
                self.server_proc.terminate()
            except Exception:
                pass
        event.accept()

if __name__ == '__main__':
    server_proc = start_local_server()
    if server_proc:
        kill_server_on_exit(server_proc)
    app = QtWidgets.QApplication(sys.argv)
    profile = QtWebEngineWidgets.QWebEngineProfile.defaultProfile()
    profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    main = SmartUkguMain(server_proc=server_proc)
    main.show()
    sys.exit(app.exec_())
