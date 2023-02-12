from repository import Repository


def run(*args, **kwargs):
    print("Run task 4")
    print(f"\t From repository '{Repository.ins().load_string('TASK_NAME')}'")
    print(f"\t From repository '{Repository.ins().load_json('OUTPUT_DICT_NAME')}'")

    file_id = Repository.ins().load_string("SAVED_FILE_ID")
    Repository.ins().load_file(file_id, "loaded_file.py")
