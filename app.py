from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Integracao com o Banco de Dados

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
db = SQLAlchemy()
db.init_app(app)

# Criacao das tabelas
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
    def __init__(self, title, complete):
        self.title = title
        self.complete = complete

# Rotas da Pagina 
@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template(
        'index.html', 
        todo_list=todo_list
        )

# Adicionar uma tarefa
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    
    if request.method == 'POST':
        newTodo = Todo(
            title, 
            False
        )
        db.session.add(newTodo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/<int:id>/update',)
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/<int:id>/delete')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    