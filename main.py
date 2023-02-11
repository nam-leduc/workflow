import json
from typing import Dict, List

from src.model import WorkflowSchema
from src.workflow_engine import WorkflowEngine


def load_workflow_def(file_path: str) -> List[Dict]:
    with open(file_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    with open("data/tasks.json") as f:
        workflow = json.load(f)

    schema = WorkflowSchema()
    workflow = schema.load(workflow)

    engine = WorkflowEngine(workflow)
    engine.run()
