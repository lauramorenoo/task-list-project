import requests

# Confirm the GET /tasks route responds successfully 
def test_get_tasks():
    response = requests.get("http://127.0.0.1:5000/tasks")
    assert response.status_code == 200
    
# Confirms the server accepts a new task and responds successully
# check the request succeeded
def test_post_task():
    tasks = {"id": 1, "status": True, "task": "Read book"}
    r = requests.post("http://127.0.0.1:5000/tasks", json=tasks)
    assert r.status_code == 200

# Checks PUT updates the task's status and responds successfully
def test_put_task():
    response = requests.put("http://127.0.0.1:5000/tasks/1")
    assert response.json()["status"] == True
    assert response.status_code == 200
        
# Checks DELETE returns 200
def test_delete_task():
    response = requests.delete("http://127.0.0.1:5000/tasks/1")
    assert response.status_code == 200
    
    response = requests.get("http://127.0.0.1:5000/tasks")
    ids = [task["id"] for task in response.json()]
    assert response.status_code == 200
    assert 1 not in ids
    