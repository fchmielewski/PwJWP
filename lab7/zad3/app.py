from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Teacher {self.name} – {self.subject}>"


# Init database and data
if not Path("app.db").exists():
    with app.app_context():
        db.create_all()
        db.session.add_all(
            [
                Task(text="Buy milk"),
                Task(text="Learn Flask", done=True),
                Teacher(
                    name="Anna Kowalska", subject="Matematyka", time="Pon 08:00-10:00"
                ),
                Teacher(name="Jan Nowak", subject="Fizyka", time="Wt 12:00-14:00"),
                Teacher(
                    name="Ewa Wiśniewska", subject="Biologia", time="Śr 09:00-11:00"
                ),
            ]
        )
        db.session.commit()


# Routes
@app.route("/")
def home():
    return render_template("index.html")


# Tasks
@app.route("/tasks", methods=["GET", "POST"])
def tasks_view():
    if request.method == "POST":
        text = request.form.get("task", "").strip()
        if text:
            db.session.add(Task(text=text))
            db.session.commit()
        return redirect(url_for("tasks_view"))

    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/done/<int:task_id>")
def mark_done(task_id: int):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for("tasks_view"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id: int):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks_view"))


# Teachers
@app.route("/teachers", methods=["GET", "POST"])
def teachers_view():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        subject = request.form.get("subject", "").strip()
        time = request.form.get("time", "").strip()
        if name and subject and time:
            db.session.add(Teacher(name=name, subject=subject, time=time))
            db.session.commit()
        return redirect(url_for("teachers_view"))

    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template("teachers.html", teachers=teachers)


@app.route("/delete_teacher/<int:teacher_id>")
def delete_teacher(teacher_id: int):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for("teachers_view"))


# About
@app.route("/about")
def about():
    return render_template("about.html")


# Run
if __name__ == "__main__":
    app.run(debug=True)
