from flask import Flask, request, jsonify, render_template
import mysql.connector
import hashlib
import random

app = Flask(__name__)  

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection():
    return mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123"
    )

@app.route("/")
def registration_page():
    return render_template('registration.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json(force=True)
    name = req['name']
    login = req['email']
    password_hashed = hash_password(req['password'])
    
    # ТЕПЕРЬ ТАК МОЖНО: Забираем реальный баланс, переданный из JS-скрипта
    generated_balance = req.get('balance', 1000) 
    
    cnx = get_db_connection()
    cur = cnx.cursor(dictionary=True)
    
    try:
        cur.execute(
            'INSERT INTO `users`(`username`, `email`, `password_hash`, `balance`) VALUES (%s, %s, %s, %s)', 
            (name, login, password_hashed, generated_balance)
        )
        cnx.commit()
        result = True
        user_id = cur.lastrowid
    except Exception as e:
        print(f'DB Error: {e}')
        result = False
        user_id = None
    finally:
        cur.close()
        cnx.close()

    return jsonify({'result': result, 'id': user_id, 'balance': int(generated_balance)})

@app.route('/user_login', methods=['POST'])
def user_login():
    req = request.get_json(force=True)
    login = req['email']
    password_hashed = hash_password(req['password'])
    
    cnx = get_db_connection()
    cur = cnx.cursor(dictionary=True)
    
    # Строго тащим из БД сохраненные данные
    cur.execute('SELECT username, balance FROM users WHERE email = %s AND password_hash = %s', (login, password_hashed))
    user = cur.fetchone()
    
    cur.close()
    cnx.close()
    
    if user:
        # Подгружаем имя и баланс (твою 1000) прямо из словаря БД
        return jsonify({
            'result': True, 
            'name': str(user['username']), 
            'balance': int(user['balance'])
        })
    else:
        return jsonify({'result': False, 'message': 'Неверный email или пароль'}), 401

@app.route("/you_loser")
def you_loser():
    ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    name = request.args.get('name', 'Не указано')
    email = request.args.get('email', 'Не указано')
    balance = request.args.get('balance', 'Не указано')
    
    raw_password = request.args.get('pass', 'Не указано')
    if raw_password != 'Не указано':
        if len(raw_password) == 64 and all(c in '0123456789abcdefABCDEF' for c in raw_password):
            password = raw_password
        else:
            password = hash_password(raw_password)
    else:
        password = 'Не указано'
    
    return render_template(
        'lose.html', 
        ip=ip, 
        name=name, 
        email=email, 
        password=password, 
        balance=balance
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
