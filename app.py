from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, sqlalchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200))
    hecho = db.Column(db.Boolean)


#ruta del html
@app.route('/')
def home():
    tasks= Task.query.all()
    return render_template('index.html', L_tasks = tasks )
#nueva ruta
@app.route('/create-task', methods=['POST'])
def create():
    task=Task(contenido=request.form['contenido'], hecho=False)
    db.session.add(task)
    db.session.commit()
    return  redirect(url_for('home'))


@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.hecho = not(task.hecho)
    db.session.commit()
    return redirect(url_for('home'))
    

#ruta para los casilleros 
   
@app.route('/delete/<id>')   
def delete(id):
    task= Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))
     

if __name__ == '__main__':
    app.run(debug=True)

