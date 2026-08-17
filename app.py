from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []  # in-memory storage — resets every time the server restarts

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.json
    task["id"] = len(tasks) + 1
    task["status"] = False
    tasks.append(task)
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = True
            return task
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)