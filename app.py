from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

# после создания класса, перейти в терминал python и прописать следующие команды
# from <название файла, в котором находится бд> import <основной объект Flask(_name_), переменную БД
# from app import app, db
# app.app_context().push()
# db.create_all()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/index')
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        post = Post(title=title, description=description)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/index")
        except:
            return 'Ошибка при добавлении статьи'
        
    else:
        return render_template("create.html")

if __name__ == '__main__':
    app.run(debug=True)