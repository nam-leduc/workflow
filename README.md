# workflow

Engine for running workflow tasks

## Contents

I want to write a workflow engine.

This engine can run tasks with functionality similar with activity diagram, it means we have two tasks type

1. normal task
2. conditional task with condition function to decide next task

All "normal task", "conditional task" and "condition function" will be implemented as python module.

Input of engine are json file which define tasks, engine will load json file.
Besides that, I can install new task doer to workflow engine.
I like the way of object-oriented and plugin mechanic implementation.

Please just write code and don't explain about the code.

## Structure

- `main_tasks_to_plantuml.py` are used for convert tasks.json to plantuml activity diagram
- `main.py` are used for load tasks.json and perform tasks
- `tasks/` are used for containing the built-in and additional tasks

## Functionality

- [Done] Run workflow by definition inside json file
- [Done] Each task can save the data
  - Save text data to local db & files to file system
  - Save text data & files to remote db
  - Access data from task runner
- [Done] Support setting task runner loading folder

## Gui

GUI to adding task to list of task.
- Support drag & drop
- Should have a toolbar on the left
- User can drag task from toolbar to drawing region
- User can connect two tasks
- User can export tasks as json with the following format
  ```json
  {
    "start_task": "tasks.task1",
    "tasks": [
      {
        "type": "normal",
        "name": "tasks.task1"
      },
      {
        "type": "conditional",
        "name": "condition_1",
        "outgoing_tasks": [
          {
            "condition": "tasks.condition1",
            "next_task": "tasks.task3"
          },
          {
            "next_task": "tasks.task4"
          }
        ]
      },
      {
        "type": "normal",
        "name": "tasks.task3"
      },
      {
        "type": "normal",
        "name": "tasks.task4"
      },
      {
        "type": "normal",
        "name": "tasks.task5"
      },
      {
        "type": "normal",
        "name": "tasks.task6"
      }
    ]
  }
  ```

Framework: Use material ui and reactjs
