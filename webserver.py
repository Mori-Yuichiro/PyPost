from flask import render_template, redirect, request, session, url_for

from app import app

# import models
from app.models import User, Post


@app.route('/', methods=["GET", "POST"])
def index():
    # トップページを表示
    if request.method == "GET":
        app.logger.info('初期表示')
        return render_template('index.html')
    elif request.method == "POST":
        app.logger.info('ユーザー登録')
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = User(username, password)
        User.save(user_data)
        app.logger.info('ユーザー登録完了')

        # Postテーブルに追加するためのユーザーID
        user_id = User.query.filter_by(name=username, password=password).first().id
        # セッションに保存
        session['user_id'] = user_id
        session['name'] = username
        session['password'] = password

        app.logger.info('ユーザーID:' + str(user_id))
        return redirect(url_for('top'))

# 全投稿表示
@app.route('/top/', methods=["GET"])
def top():
    if request.method == "GET":
        app.logger.info('全投稿表示')

        contents = Post.query.all()
        # 投稿保存用の配列
        posts = []
        id = 1
        for content in contents:
            postDataStr = str(content)[5:]
            postData = {'id':id, 'content':postDataStr}
            posts.append(postData)
            id += 1
       
        app.logger.info('ユーザーID:' + str(session['user_id']))
        return render_template('top.html', user_name=session['name'], posts=posts)

# 新規投稿
@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "GET":
        app.logger.info('新規投稿ページ表示')
        
        return render_template('post.html')
    elif request.method == "POST":
        content = request.form.get('post')

        user = User.query.filter_by(id=session['user_id']).first()
        app.logger.info(user.id)

        post_data = Post(content=content, user_id=user.id)
        Post.post(post_data)
       
        postContent = Post.query.all()
        app.logger.info(postContent)
        
        # 投稿保存用の配列
        posts = []
        id = 1
        # 配列に投稿を格納
        for content in postContent:
            postDataStr = str(content)[5:]
            postData = {'id':id, 'content':postDataStr}
            posts.append(postData)
            id += 1

        app.logger.info('新規投稿完了')

        return render_template('top.html', user_name=session['name'], posts=posts)
# 投稿削除
@app.route('/delete', methods=['POST'])
def delete():
    from app import db

    id = request.form.get('id')
    print("削除ID取得:" + str(id))
    Post.query.filter_by(id=id).delete()

    app.logger.info('削除完了。ID:' + str(id))

    db.session.commit()

    posts = Post.query.all()
    return render_template('top.html', user_name=session['name'], posts=posts)

# プログラム開始
def start():
    # app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
    app.run(debug=True)
