from flask import flash, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, Post
from app import app

#
#User
#
#Register user
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
        except Exception as e:
            app.logger.info(e.args)
            return redirect(url_for('index'))

#Login
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

@app.route('/deluser', methods=["POST"])
@login_required
def delUser():
    if request.method == 'POST':
        app.logger.info('ユーザー削除')
        #ユーザー情報を取得
        id = request.form.get('user_id')
        user = User.query.filter_by(id=id).first()
        app.logger.info('ユーザー：' + user.name)
        User.delUser(user)
        app.logger.info('ユーザー削除完了')

        return redirect(url_for('index'))


#Top page
@app.route('/top', methods=['GET'])
@login_required
def toppage():
    # ログインしたユーザー情報を取得
    user = User.query.filter_by(name=current_user.name, password=current_user.password).first()
    app.logger.info('ユーザーネーム:' + user.name)

    #投稿情報取得
    posts = User.query.filter_by(name=current_user.name, password=current_user.password).first().posts

    return render_template('top.html', user_id=user.id, user_name=user.name, posts=posts)


#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info('ログアウト成功')

    return redirect(url_for('login'))


#
#Post
#
@app.route('/post', methods=["GET", "POST"])
@login_required
def post():
    #投稿ページを表示
    if request.method == "GET":
        app.logger.info('投稿ページ表示')
        return render_template('post.html')

    #投稿
    elif request.method == "POST":
        try:
            app.logger.info('投稿')
            app.logger.info('投稿内容:' + request.form.get('post'))

            #Postテーブルに保存するuser情報を取得
            user = User.query.filter_by(name=current_user.name, password=current_user.password).first()
            #投稿を保存
            post = Post(content=request.form.get('post'), user_id=user.id)
            Post.post(post)
            app.logger.info('投稿完了')

            return redirect(url_for('toppage'))
        except Exception as e:
            app.logger.info(e.args)
            return redirect(url_for('post'))

#投稿を削除
@app.route('/delete', methods=["POST"])
def delPost():
    id = request.form.get('id')
    post = Post.query.filter_by(id=id).first()
    app.logger.info('削除投稿:' + post.content)
    Post.delPost(post)
    app.logger.info('削除完了')

    return redirect(url_for('toppage'))


# プログラム開始
def start():
    app.run(debug=True)
