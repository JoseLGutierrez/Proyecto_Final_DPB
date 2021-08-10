from flask import Flask, render_template, request, redirect, url_for  #debemos importarlo  todo esto
from flask_sqlalchemy import SQLAlchemy, sqlalchemy  #Es muy necesario que tengas instalado tu SQLAlchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):                                        #Creacion de la clase task
    id =db.Column(db.Integer, primary_key=True)              # el id de cada elemento agregado
    contenido = db.Column(db.String(200))                    #la clase de contenido
    hecho = db.Column(db.Boolean)                            #La columna para ver los datos


#ruta del html
@app.route('/')
def home():
    tasks= Task.query.all()
    return render_template('index.html', L_tasks = tasks )
    
#nueva ruta para crear 
@app.route('/create-task', methods=['POST'])
def create():
    task=Task(contenido=request.form['contenido'], hecho=False)
    db.session.add(task)
    db.session.commit()
    return  redirect(url_for('home'))

# en esta parte del codigo se va a definir para que se pueda validar o no el 'hecho' o deshacer
@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.hecho = not(task.hecho)
    db.session.commit()
    return redirect(url_for('home'))
    

#En esta parte del codio se crea la definicion para poder borrar los datos creados
   
@app.route('/delete/<id>')   
def delete(id):
    task= Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))
     

if __name__ == '__main__':
    app.run(debug=True)

