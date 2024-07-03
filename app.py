import json

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
from config import Config
from models import db, User, Class_time_table
import sqlite3
from sqlalchemy import Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)




def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    pattern = r"^\+?\d{10,15}$"
    return re.match(pattern, phone) is not None


@app.route('/')
def home():

    class_time_tables = Class_time_table.query.all()

    return render_template('home.html', class_time_tables=class_time_tables)


@app.route('/admin', methods=['GET'])
def admin():
    if 'username' not in session or session['username'] != 'admin':  # 假设管理员的用户ID为1
        return jsonify({'message': 'Unauthorized'}), 401
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'user_id' not in session or session['user_id'] != 1:
        return jsonify({'message': 'Unauthorized'}), 401
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


@app.route('/user/add', methods=['POST'])
def add_user():
    if 'user_id' not in session or session['user_id'] != 1:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.json
    username = data['username']
    email = data['email']
    phone = data['phone']
    password = data['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409
    if User.query.filter_by(phone=phone).first():
        return jsonify({'message': 'Phone already exists'}), 409

    user = User(username=username,email=email,phone=phone,password=password)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201


@app.route('/user/update/<int:username>', methods=['POST'])
def update_user(username):
    if 'user_id' not in session or session['user_id'] != 1:
        return jsonify({'message': 'Unauthorized'}), 401
    user = User.query.get_or_404(username)
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    if username:
        user.username = username
    if email:
        user.email = email
    if phone:
        user.phone = phone
    if password:
        user.password = password
        user.set_password(password)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


@app.route('/tables', methods=['GET'])
def get_tables():

    if 'user_id' not in session or session['user_id'] != 1:
        return jsonify({'message': 'Unauthorized'}), 401
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)


# 获取指定表名的数据
@app.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    if 'user_id' not in session or session['user_id'] != 1:
        return jsonify({'message': 'Unauthorized'}), 401
    table = Table(table_name, db.metadata, autoload=True, autoload_with=db.engine)
    query = db.session.query(table)
    data = query.all()
    # 将查询结果转换为字典列表
    results = [{column.name: getattr(row, column.name) for column in table.columns} for row in data]
    return jsonify(results)





# @app.route('/home')
# def home():
#     return render_template('home.html')


@app.route('/bazi_mingli', methods=['GET', 'POST'])
def bazi_mingli():
    return render_template('bazi_mingli.html')


@app.route('/fengshui_xuanxue', methods=['GET', 'POST'])
def fengshui_xuanxue():
    return render_template('fengshui_xuanxue.html')


@app.route('/fengshui_xuanxue', methods=['GET', 'POST'])
def zhuanti1():
    return render_template('zhaunti1.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_contact = request.form['username_or_contact']
        password = request.form['password']

        user = User.query.filter(
            (User.username == username_or_contact) |
            (User.email == username_or_contact) |
            (User.phone == username_or_contact)
        ).first()

        if user and user.password == password:
            session['user_id'] = user.id

            session['username'] = user.username
            flash('登录成功!')
            return redirect('/')
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))

        if not validate_email(email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('register'))

        if not validate_phone(phone):
            flash('Invalid phone number format.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(phone=phone).first():
            flash('Phone number already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect('/')


@app.route('/api/button1', methods=['GET'])
def api_button1():
    return jsonify({'message': 'Button 1 clicked!', 'data': 'data'})


@app.route('/api/button2', methods=['GET'])
def api_button2():
    return jsonify({'message': 'Button 2 clicked!'})


@app.route('/http://127.0.0.1:7862/chat/knowledge_base_chat', methods=['POST'])
def api_button3():
    return jsonify({'message': 'Button 3 clicked!'})


@app.route('/http://localhost:7862/knowledge_base/list_knowledge_bases', methods=['GET'])
def api_button4():
    return jsonify({'message': 'Button 4 clicked!'})


@app.route('/api/user_info', methods=['GET'])
def user_info():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    user = User.query.get(session['user_id'])
    return jsonify({
        'username': user.username,
        'email': user.email,
        'phone': user.phone
    })


# @app.route('/api/button5', methods=['GET'])
# def api_button5():
#     # if 'user_id' not in session:
#     #     return jsonify({'error': 'Not authenticated'}), 401
#     # user = User.query.get(session['user_id'])
#     if 'user_id' not in session:
#         flash('You need to login first.', 'danger')
#         return redirect(url_for('login'))
#
#     user = User.query.get(session['user_id'])
#     return render_template('/chat', user=user)


@app.route('/chat', methods=['GET', 'post'])
def chat():
    if 'user_id' not in session:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('chat.html', user=user)


"""
    POST请求，带参数
"""


@app.route('/api/knowledge_chat', methods=['GET', 'POST'])
def knowledge_chat():
    if request.method == 'POST':
        query = request.form['query']
        return jsonify({
            "query": query,
            "knowledge_base_name": "fengshui",
            "top_k": 3,
            "pdf_name": "string",
            "score_threshold": 1,
            "history": [
                {
                    "role": "user",
                    "content": "我们来玩成语接龙，我先来，生龙活虎"
                },
                {
                    "role": "assistant",
                    "content": "虎头虎脑"
                }
            ],
            "stream": False,
            "model_name": "xinghuo-api",
            "temperature": 0.7,
            "max_tokens": 0,
            "prompt_name": "default"
        })


@app.route('/second_page')
def secondpage():
    return render_template('bazi_mingli.html')


if __name__ == '__main__':
    app.run(debug=True, port=50001, threaded=True)
