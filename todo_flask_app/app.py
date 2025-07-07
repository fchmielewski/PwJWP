from itertools import count
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In‑memory store
_id = count(1)
tasks: list[dict] = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks_view():
    if request.method == "POST":
        text = request.form.get("task", "").strip()
        if text:
            tasks.append({"id": next(_id), "text": text, "done": False})
        return redirect(url_for("tasks_view"))
    return render_template("tasks.html", tasks=tasks)

@app.route("/done/<int:task_id>")
def mark_done(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    return redirect(url_for("tasks_view"))

@app.route("/delete/<int:task_id>")
def delete(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("tasks_view"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)