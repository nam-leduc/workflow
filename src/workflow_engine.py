import importlib
import logging
import sys
from abc import abstractmethod

from . import model

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)


class Task:
    @abstractmethod
    def run(self, inputs: dict):
        pass


class NormalTask(Task):
    def __init__(self, task: model.NormalTask):
        self._model = task

    def run(self, inputs: dict):
        logging.info("Running normal task")
        task_fnc = load_condition_module(self._model.name)
        task_fnc(inputs)


def load_condition_module(condition_module):
    logging.info(f"Loading {condition_module}.run(*args, **kwargs)")
    module = importlib.import_module(condition_module)
    return getattr(module, "run")


def default_condition():
    pass


class ConditionalTask(Task):
    def __init__(self, task: model.ConditionalTask):
        self._model: model.ConditionalTask = task

    def run(self, inputs: dict):
        logging.info("Run conditional task")

        task = self._get_matched_task_using_condition()
        if task:
            return task.next_task

        default_next_task = self.get_default_next_task()
        if default_next_task:
            logging.info(f"There are no condition matched, we use default next task '{default_next_task}'")
            return default_next_task

        raise Exception(f"Can't find any matched condition of {self._model.name}")

    def _get_matched_task_using_condition(self):
        matched_task = None
        for task in self._model.outgoing_tasks:
            if not task.condition:
                continue
            condition = load_condition_module(task.condition)

            if condition():
                logging.info(f"Matched with condition {task.condition}, next task is {task.next_task}")
                matched_task = task
                break
        return matched_task

    def get_default_next_task(self):
        default_next_task = next(
            (task.next_task for task in self._model.outgoing_tasks if task.condition is None),
            None
        )
        return default_next_task


class WorkflowEngine:
    def __init__(self, workflow: model.Workflow):
        # Mapping to task
        self._task_map = {}

        # Contain list of task name which will run one by one
        self._task_list = []
        self._wf_data = {}
        self._workflow = workflow

        self._load_tasks()

    def _load_tasks(self):
        for model_task in self._workflow.tasks:
            if isinstance(model_task, model.NormalTask):
                task = NormalTask(model_task)
            elif isinstance(model_task, model.ConditionalTask):
                task = ConditionalTask(model_task)
            else:
                raise Exception(f"unknown json task {model_task}")
            self._task_map[model_task.name] = task
            self._task_list.append(model_task.name)

        logging.info(f"Task map: {list(self._task_map.keys())}")
        logging.info(f"Task list: {self._task_list}")

    def run(self):
        task_idx = self._task_list.index(self._workflow.start_task)
        while task_idx < len(self._task_list):
            task_name = self._task_list[task_idx]
            task = self._task_map[task_name]

            logging.info(f"Run at {task_idx} by using task {task_name}")

            if isinstance(task, NormalTask):
                task.run(self._wf_data)
                task_idx += 1
            elif isinstance(task, ConditionalTask):
                next_task_name = task.run(self._wf_data)
                task_idx = self._task_list.index(next_task_name)
            else:
                raise Exception(f"unknown task type {task}")
