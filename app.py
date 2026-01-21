from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ToDo {self.SNo} - {self.title}>"
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_todo = ToDo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
    todos = ToDo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/show')
def show():
    todos = ToDo.query.all()
    print(todos)
    return "Check console for ToDo items."

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(SNo=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit(sno):  
    todo = ToDo.query.filter_by(SNo=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', todo=todo)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')