# save_server.py
from flask import Flask, request, jsonify
import json
from pathlib import Path



app = Flask(__name__)
DATA_FILE = Path("smartukgu-desktop") / "src" / "data" / "account_info.json"

@app.route("/save_login", methods=["POST"])
def save_login():
    data = request.json
    login = data.get('login', '')
    password = data.get('password', '')
    iin = login if len(login) == 12 and login.isdigit() else ''
    info = {'login': login, 'password': password, 'iin': iin}
    DATA_FILE.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
    return jsonify({"status": "ok", "msg": "Данные сохранены"})

@app.route("/get_login", methods=["GET"])
def get_login():
    if DATA_FILE.exists():
        try:
            info = json.loads(DATA_FILE.read_text(encoding='utf-8'))
            return jsonify(info)
        except Exception:
            pass
    # Если файл пустой или сломан
    return jsonify({"login": "", "password": "", "iin": ""})

if __name__ == '__main__':
    # Хост и порт строго по твоему запросу
    app.run(host="127.0.0.1", port=5000, debug=False)
