from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    deadline = db.Column(db.String(25),nullable=False)
    date_created = db.Column(db.DateTime,default= datetime.utcnow)
    

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET']) 
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_dead = request.form['deadline']
        new_task = Todo(content=task_content,deadline=task_dead)
        try:
            db.session.add(new_task)
            db.session.commit()
           
            return redirect('/')
        except:
            return "no"
    else:
        task = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',task = task)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem deleting'
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update_t(id):

        task_up = Todo.query.get_or_404(id)
        if request.method == 'POST':
            task_up.content = request.form['content']
            task_up.deadline = request.form['deadline']
          
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "It failed to update"
        else:   
          return render_template('update.html',task=task_up)
        
        
        
      
        


if __name__ == "__main__": 
    app.run(debug=True)