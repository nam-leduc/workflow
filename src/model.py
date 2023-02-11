from typing import List

import marshmallow as mm
from marshmallow import fields
from marshmallow.fields import String as MString, Nested as MNested, List as MList


class OutgoingTaskSchema(mm.Schema):
    condition = MString(allow_none=True)
    next_task = MString(required=True)

    @mm.post_load
    def make_outgoing_task(self, data, **kwargs):
        return OutgoingTask(**data)


class OutgoingTask:
    def __init__(self, next_task, condition=None, **kwargs):
        self.condition = condition
        self.next_task = next_task


class TaskSchema(mm.Schema):
    type = MString(required=True)
    name = MString(required=True)
    outgoing_tasks = MList(MNested(OutgoingTaskSchema(), allow_none=True))

    @mm.post_load
    def make_task(self, data, **kwargs):
        if data["type"] == "normal":
            return NormalTask(**data)
        elif data["type"] == "conditional":
            return ConditionalTask(**data)


class BaseTask:
    def __init__(self, type_, name, **kwargs):
        self.type = type_
        self.name = name


class NormalTask(BaseTask):
    def __init__(self, **kwargs):
        super().__init__("normal", **kwargs)


class ConditionalTask(BaseTask):
    def __init__(self, outgoing_tasks, **kwargs):
        super().__init__("condition", **kwargs)
        self.outgoing_tasks: List[OutgoingTask] = outgoing_tasks


class WorkflowSchema(mm.Schema):
    start_task = MString(required=True)
    tasks = MList(MNested(TaskSchema(), required=True))

    @mm.post_load
    def make_workflow(self, data, **kwargs):
        return Workflow(**data)


class Workflow:
    def __init__(self, start_task, tasks):
        self.start_task: str = start_task
        self.tasks: List[BaseTask] = tasks
