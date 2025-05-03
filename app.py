from flask import Flask, render_template, request, redirect

app = Flask(__name__)
TODO_FILE = "todo.txt"

def read_tasks():
    try:
        with open(TODO_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        file.writelines(tasks)

@app.route("/")
def index():
    tasks = read_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    with open(TODO_FILE, "a") as file:
        file.write(f"[ ] {task}\n")
    return redirect("/")

@app.route("/done/<int:index>")
def mark_done(index):
    tasks = read_tasks()
    if "[ ]" in tasks[index]:
        tasks[index] = tasks[index].replace("[ ]", "[x]", 1)
        write_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    tasks = read_tasks()
    tasks.pop(index)
    write_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
