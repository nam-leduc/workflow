import uuid

from repository import Repository


def run(*args, **kwargs):
    print(f"Run task 1")
    Repository.ins().save_string("TASK_NAME", "From task 1")
    Repository.ins().save_json("OUTPUT_DICT_NAME", {"name": "My Name"})
    file_id = str(uuid.uuid4())
    Repository.ins().save_file(file_id, __file__)
    Repository.ins().save_string("SAVED_FILE_ID", file_id)
