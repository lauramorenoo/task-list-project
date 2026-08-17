# QA Portfolio Project — Task List API with CRUD and Automated Tests

This is a backend-only project — no front-end included. A small Flask API for managing tasks, with a full automated test suite covering the API.

## What This Project Demonstrates
- Automated API testing with pytest and requests
- Full CRUD operations (Create, Read, Update, Delete) via a REST API
- CI/CD pipeline using GitHub Actions (tests run automatically on every push)
- RESTful API design (Flask)

## Tech Stack
Python, Flask, pytest, Git, GitHub

## Project Structure
```
app.py — Flask REST API with GET/POST/PUT/DELETE endpoints for managing tasks
test_app.py — pytest suite testing the API directly (status codes, response data)
```

## How to Run Locally
```
git clone https://github.com/lauramorenoo/task-list-project.git
cd task-list-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run the Tests
Terminal 1 (start the server):
```
source venv/bin/activate
python3 app.py
```

Terminal 2 (run tests):
```
source venv/bin/activate
pytest test_app.py -v
```

## Continuous Integration
Tests run automatically via GitHub Actions on every push.

## Future Improvements
- Allow PUT to toggle status back and forth (complete <-> incomplete), not just one-way — real use case: a recurring weekly task list that needs to reset once the week is done
- 404 handling / empty-list messaging