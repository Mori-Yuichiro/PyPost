from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import app

from app.models import User


@app.route('/', methods=["GET", "POST"])
def index():
    # トップページを表示
    if request.method == "GET":
        app.logger.info('初期表示')
        return render_template('index.html')
    elif request.method == "POST":
        try:
            app.logger.info('ユーザー登録')
            username = request.form.get('username')
            password = request.form.get('password')

            if User.query.filter_by(name=username, password=password).first() is not None:
                flash('その名前もしくはパスワードはすでに登録されています。登録し直してください。')
                return render_template('index.html')

            user_data = User(username, password)
            User.save(user_data)
            app.logger.info('ユーザー登録完了')

            # Postテーブルに追加するためのユーザーID
            user_id = User.query.filter_by(name=username, password=password).first().id
            login_user(user_data)

            app.logger.info('ユーザーID:' + str(user_id))
            return redirect(url_for('login'))
        except:
            return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        app.logger.info('ログインページ')
        return render_template('login.html')
    elif request.method == "POST":
        app.logger.info('ログイン認証開始')
        
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=username, password=password).first()

        if user is not None:
            login_user(user)
            app.logger.info('ログイン成功')
            flash('ログインに成功しました')

            return redirect(url_for('toppage'))
        else:
            app.logger.info('ログインに失敗しました')

            flash('ログインに失敗しました')
            return redirect(url_for('login'))

@app.route('/top', methods=['GET'])
@login_required
def toppage():
    # ログインしたユーザー情報を取得
    user = User.query.filter_by(name=current_user.name, password=current_user.password).first()
    app.logger.info('ユーザーネーム:' + user.name)

    return render_template('top.html', user_name=user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info('ログアウト成功')

    return redirect(url_for('login'))


# プログラム開始
def start():
    app.run(debug=True)
