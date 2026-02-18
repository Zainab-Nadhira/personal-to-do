from flask import Flask, render_template, request, redirect, url_for
import csv, os

app = Flask(__name__)
TASK_FILE = 'tasks.csv'

# Load tasks and include CSV index
def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for idx, row in enumerate(reader):
                if row:
                    tasks.append({'task': row[0], 'done': row[1]=='True', 'index': idx})
    return tasks

# Save tasks back to CSV
def save_tasks(tasks):
    with open(TASK_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for t in tasks:
            writer.writerow([t['task'], t['done']])

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    
    # Add task
    if request.method == "POST":
        new_task = request.form.get("task")
        if new_task:
            tasks.append({'task': new_task, 'done': False, 'index': len(tasks)})
            save_tasks(tasks)
        return redirect(url_for('index'))

    # Sorting
    sort_option = request.args.get('sort', 'pending')
    if sort_option == 'alpha':
        tasks.sort(key=lambda x: x['task'].lower())
    elif sort_option == 'newest':
        tasks = tasks[::-1]  # newest first
    else:  # pending first
        tasks.sort(key=lambda x: x['done'])

    pending_count = sum(not t['done'] for t in tasks)
    return render_template("index.html", tasks=tasks, pending_count=pending_count, sort_option=sort_option)

@app.route("/done/<int:task_id>")
def done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['index'] == task_id:
            t['done'] = not t['done']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['index'] != task_id]
    # Reassign indexes
    for idx, t in enumerate(tasks):
        t['index'] = idx
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
