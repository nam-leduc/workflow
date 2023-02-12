import json

from src.model import WorkflowSchema
from src.workflow_engine import WorkflowEngine


def test_run_workflow():
    print()

    with open("test_data/data/tasks.json") as f:
        workflow = json.load(f)

    schema = WorkflowSchema()
    workflow = schema.load(workflow)

    engine = WorkflowEngine(workflow)
    engine.set_tasks_container_directory("test_data/tasks")
    engine.run()
    engine.destroy()
