# Task List Project — Progress Notes

## Setup
- Project folder: `task-list-project` — SEPARATE from `qa-portfolio-project`, own fresh venv
- Activate venv: `source venv/bin/activate`
- Confirm venv is active: `which python3` → should point inside `.../task-list-project/venv/bin/python3`
- Each new project needs its OWN `pip install` — nothing carries over between venvs, even if a
  package (like Flask) was already installed in a different project. This is intentional/good —
  keeps each project's dependency versions isolated from each other, no cross-project conflicts.
- Installed so far: `flask`

---

## Session 1 — Designing and building the API ✅ DONE (core CRUD complete)

**Goal:** Practice the same pattern as the first project (Flask API + routes) but with LESS
hand-holding — designed the routes and data shape myself before writing any code.

**Routes designed and built:**
- `GET /tasks` — returns all tasks
- `POST /tasks` — creates a new task
- `PUT /tasks/<task_id>` — marks a task complete (new — wasn't in the first project)
- `DELETE /tasks/<task_id>` — removes a task (new — wasn't in the first project)

**Data shape:** `{"id": int, "status": bool, "task": string}`
- Used `True`/`False` (boolean) for status instead of a string like `"done"` — easier to check/set
  in code than matching against arbitrary text

**New concepts learned:**
- `PUT` = update something that already exists (as opposed to `POST` = create new)
- `DELETE` = remove something — and its route usually doesn't need to return data back (nothing
  left to show), just a confirmation message like `{"message": "Task deleted"}`
- Lists have `.remove(item)` to delete a specific item — mirror of `.append()` for adding one

**Bugs I hit and fixed:**
- `method=[...]` instead of `methods=[...]` — repeated typo across a couple routes, good one to
  watch for automatically now
- Route type mismatch: tried `<boolean:task_id>` at first — URL id types should be `<int:...>`,
  not the data type of an unrelated field
- Loop/if logic mixed up matching-the-task with checking-the-status — took a few passes to
  separate "find the right task by id" (the `if` condition) from "what to do once found" (the
  action inside the if)
- `task["status"] == True` / `is True` — CHECKS a value, doesn't SET one. Needed `=` (assignment)
  to actually change status to True. Same `==` vs `=` trap as last project's id-generation bug.
- Indentation/return placement in `remove_task` — took several attempts to get the "not found"
  fallback `return` positioned correctly OUTSIDE both the `for` and the `if` (same rule as
  `get_item` from the first project: a fallback return only runs if the loop finishes with no
  match — it needs to line up with `for`, not be nested inside it)
- **Big one — missing `if __name__ == "__main__": app.run(debug=True)` at the bottom of `app.py`.**
  Without it, the file runs top to bottom, defines all the routes, and just... stops. No error,
  no "Running on..." message — just silently returns to the terminal prompt. If `python3 app.py`
  ever exits immediately with zero output, this is the first thing to check.
- **Real gap in `add_task()`, caught after testing:** originally only set `id`, forgot to also
  default `status` to `False` on creation — meant tasks had no status field at all until PUT was
  called on them. Fixed by adding `task["status"] = False` alongside the id assignment.
  **Lesson:** whenever a data shape is planned upfront (like `{id, status, task}`), double-check
  the "create" function actually sets EVERY field in that shape — easy to silently miss one.

**Folder mixup:** `app.py` somehow ended up created inside `venv/` instead of the project root —
likely from being in the wrong directory when creating the file/running venv setup. Fixed with
`mv venv/app.py .` Lesson: always double check location (`pwd`, `ls`) right after creating a new
project, before writing code.

**All 4 routes tested and confirmed working via curl:**
```
curl http://127.0.0.1:5000/tasks
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"task": "Read book"}'
curl -X PUT http://127.0.0.1:5000/tasks/1
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

---
## Session 2 — pytest suite for the API ✅ DONE

Built `test_app.py` with 4 tests covering all routes, done mostly independently this time —
only needed guidance on WHERE to look for bugs, not the actual fixes.

**Tests built:**
- `test_get_tasks` — GET /tasks returns 200
- `test_post_task` — POST /tasks returns 200
- `test_put_task` — PUT actually flips status to True (checks response content, not just status code)
- `test_delete_task` — DELETE actually removes the task (confirmed via follow-up GET + membership
  check, not just checking the delete request itself returned 200)

**Bugs I hit and fixed (mostly solo):**
- Ran `python3 test_app.py` instead of `pytest test_app.py` — remembered on my own that pytest
  is the actual command to run tests, not plain python3
- 405 on PUT → forgot to include the task id in the URL (`/tasks` instead of `/tasks/1`) —
  405 specifically means "this URL exists but doesn't support the method/isn't shaped right",
  different from 404 ("nothing here at all")
- 404 on DELETE → copied a `/tasks/1/delete` URL pattern from an outside article/tutorial, but
  my actual `app.py` route is just `/tasks/<int:task_id>` with the DELETE method attached —
  no `/delete` in the path at all
- **Key lesson from that DELETE bug:** tutorials/articles show valid patterns, but they're not
  universal rules — every API's URL structure is a choice made by whoever built it. Always check
  the ACTUAL route defined in app.py, don't assume a URL shape from an outside example.
- Sent unnecessary `data={...}` in the PUT test — tested removing it and confirmed the route
  doesn't use `request.json` at all (only reads `task_id` from the URL), so it was doing nothing.
  Lesson: verify empirically what a route actually reads, rather than assuming based on a tutorial.

**New pattern learned — checking a list DOESN'T contain something:**
```python
response = requests.get("http://127.0.0.1:5000/tasks")
ids = [task["id"] for task in response.json()]  # list comprehension — pulls just the ids out
assert 1 not in ids  # confirms task 1 truly isn't in the list anymore
```
- List comprehension `[task["id"] for task in response.json()]` is a compact way of writing:
  ```python
  ids = []
  for task in response.json():
      ids.append(task["id"])
  ```
- Checking "is this GONE from a list" needs BOTH pieces: pull out just the relevant field first
  (here: ids), then use `not in` to check absence — checking status_code alone doesn't prove
  the actual data changed, just that the server responded without erroring
- This took several attempts to land on the right syntax — a genuinely harder pattern than
  previous asserts (two concepts stacked: extracting data + membership check), not a sign of
  not understanding the underlying logic

**Big-picture lesson from this session:** a test that only checks `status_code == 200` can pass
even when the underlying action completely failed (e.g. delete "succeeding" on the request level
while doing nothing to the actual data). Always ask: if this specific route had a real bug, would
my test actually catch it, or would it still pass anyway?

---
## Session 3 — Git, CI, and README ✅ DONE — project fully complete

Led most of this myself from memory (git flow, .gitignore contents, workflow file structure) —
came together much faster than project 1 since the pattern was already familiar.

**What got done:**
- `.gitignore` (venv/, __pycache__/, *.pyc, AND .pytest_cache/ — new one I caught myself, since
  pytest creates this folder too and it hadn't come up in project 1)
- Git init, GitHub repo created, pushed
- `requirements.txt` generated and pushed
- `.github/workflows/tests.yml` — wrote it from memory, correctly recognized it needed almost no
  changes from project 1's version since the underlying shape (get code → get Python → install
  deps → start server → run tests) is the same regardless of project specifics
- README written mostly independently, following the same outline/structure as project 1

**Bugs hit and fixed:**
- `git push` alone failed with "fatal: No configured push destination" → hadn't yet linked local
  repo to the new GitHub repo. Fixed with `git remote add origin <url>`, confirmed via
  `git remote -v`, then `git push -u origin main` (the `-u` flag only needed on the very first
  push per repo — plain `git push` works after that)
- CI failed: `pytest: command not found` → checked `pip list` locally and discovered pytest
  wasn't actually installed in THIS project's venv at all (even though tests had been running
  successfully earlier — unclear exactly how/why, possibly a leftover pytest from PATH/another
  env at the time). Comparing local `pip list` output against `requirements.txt` line-by-line
  was the actual debugging method that caught it — genuinely useful technique: when CI says a
  package is missing, check `pip list` locally FIRST, then compare against requirements.txt,
  rather than assuming the file is just stale.
  Fixed with `pip install pytest`, then regenerated `requirements.txt` fresh.

**Key lesson reinforced this session:** once you understand the SHAPE of a CI pipeline (not just
memorized commands), it transfers almost unchanged to a new project — confirmed by how little
the tests.yml file needed to change from project 1.

---

## PROJECT STATUS: COMPLETE ✅
- Working CRUD API (all 4 methods: GET, POST, PUT, DELETE)
- Meaningful pytest suite (checks actual behavior/content, not just status codes)
- CI pipeline running on every push
- README written and pushed
- Repo: https://github.com/lauramorenoo/task-list-project

## Still true from Session 1 — Future Improvements (not built, noted for later)
- [ ] Allow PUT to toggle status back and forth (complete <-> incomplete)
- [ ] 404 handling / empty-list messaging

## Next steps (planned, not started)
- [ ] A bigger, more "real-world scenario" THIRD project — details/scope to be figured out fresh,
      not rushed at the end of a long session
- [ ] Revisit the verbal 90-second interview walkthrough — now have TWO complete projects to
      draw from, may be easier than trying with just one
- [ ] Still want more repetition/comfort with the browser (JS) <-> server (Python) handoff
      concept before it comes up again in a future front-end
---

## Future Improvements (noted for later, not built yet)
- [ ] Allow PUT to toggle status back and forth (complete <-> incomplete), not just one-way —
      real use case: a recurring weekly task list that needs to reset once the week is done
- [ ] 404 handling / empty-list messaging (same idea as first project)

---

## What's left for this project
- [ ] Decide if this project gets a front-end + Selenium tests, or stays API-only
- [ ] Git init, GitHub repo, requirements.txt, CI workflow
- [ ] README

## Questions / things to revisit
- Still want more repetition on the browser (JS) <-> server (Python) handoff concept from project 1
  before diving into a front-end for this one, if this project ends up getting one