from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    case_number = db.Column(db.String)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    date_deadline = db.Column(db.DateTime)

    def __init__(self, case_number, content, date_deadline):
        self.case_number = case_number 
        self.content = content
        self.date_deadline = date_deadline

    #def __repr__(self):
    #    return "<Task %r>" % self.id 

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
      if not request.form['case_number'] or not request.form['content'] or not request.form['date_deadline']:
         flash('Please enter all the fields', 'error')
      else:
         task = Todo( case_number = request.form['case_number'], content = request.form['content'],
           date_deadline = datetime.strptime(request.form["date_deadline"], "%Y-%m-%d"))
         
         db.session.add(task)
         db.session.commit()
         #flash('Record was successfully added')
         return redirect('/')
         
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks = tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        date_dl = datetime.strptime(request.form["date_deadline"], "%Y-%m-%d")
        task.date_deadline = date_dl  

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"

    else:
         return render_template("update.html", task = task)  


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
