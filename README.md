# StudentDigitalTool


# SmartUkgu Desktop Application

[! [SMART UKGU] (https://smart.ukgu.kz/assets/logos/logo-dark-350x350.png)] (https://smart.ukgu.kz/ru)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-brightgreen?logo=qt)](https://pypi.org/project/PyQt5/)
[![Flask](https://img.shields.io/badge/Backend-Flask-orange?logo=flask)](https://pypi.org/project/Flask/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-3333cc?logo=windows)]()
[![Status](https://img.shields.io/badge/status-actively--developed-success)]()
[![Open in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open%20Now-blue?logo=github)](https://github.com/features/codespaces)

---

> <img src="https://img.shields.io/badge/🌐%20SmartUKGU%20-%20Desktop%20версия%20онлайн%20университета%20-синий?style=for-the-badge" height="30"/>

---

<div align="center">
  
  <img src="assets/screenshot.png" alt="SmartUkgu Desktop Screenshot" width="70%" style="border-radius:18px; box-shadow:0 0 12px #23243c40;">
  
</div>

---

##  Структура проекта

## plaintext
smartukgu-desktop/
├── src/
│   ├── main.py           # Главный модуль
│   ├── save_server.py    # Локальный мини-сервер Flask
│   ├── ui/               # UI-компоненты (по желанию)
│   └── assets/           # Иконки, изображения, статические файлы
├── requirements.txt      # Зависимости проекта
├── LICENSE
└── README.md
 Быстрый старт
bash
Копировать
Редактировать
# 1. Клонируй проект
git clone <repository-url>
cd smartukgu-desktop

# 2. (Опционально) Создай виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Запусти приложение
python src/main.py
🖥 Основные возможности
<div style="background: #e9f5ff; border-radius: 10px; padding: 14px 20px 10px 20px; margin-bottom:18px">
 Веб-интерфейс SmartUKGU прямо из десктопного окна

 Локальное хранение пароля и ИИН в json-файле

 Авто-заполнение формы входа (по желанию)

🛡 Мини-сервер Flask для хранения данных (работает офлайн)

🖱Toolbar и меню: быстрый переход к расписанию, чату, новостям, калькулятору

 Красивые иконки в шапке и в меню

 Автоматическое и ручное сохранение данных аккаунта

🏳 Тёмная тема интерфейса (при поддержке OS)

 Легко расширяемая архитектура

</div>
 <span style="color:#1b9dff">Пример окна</span>
Скриншот твоего приложения:


 Зависимости
PyQt5

PyQtWebEngine

Flask

Pillow — для работы с иконками

см. requirements.txt

 Документация и советы
⚠ Все пользовательские данные (пароль/ИИН) сохраняются локально в зашифрованном виде и не передаются третьим лицам!

Пользуйся всегда своей персональной копией — данные только у тебя.

 Контрибьютинг
Форкай —> Ветки —> PR

Залетай с фичами, багами и идеями в Issues

Приветствуется качественный код и внятные коммиты

 Лицензия

Лицензия на использования бесплатно! Дорогой мой студент!
Остались вопросы?
Оставляй их в Issues — здесь помогают не по-ботовски!

Время ускорять цифровой Казахстан вместе — вноси вклад, делись знаниями, прокачивай опыт! #
