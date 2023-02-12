import os
import shutil
import uuid
from os import mkdir
from os.path import join, basename, isfile, exists


class Repository:
    _ins: "Repository" = None

    def __init__(self):
        self._str_data = {}
        self._json_data = {}
        self._file_data = {}
        self._storage_folder = "WorkflowStorage"

        if not exists(self._storage_folder):
            mkdir(self._storage_folder)

    @classmethod
    def ins(cls):
        if cls._ins is None:
            cls._ins = Repository()
        return cls._ins

    def save_file(self, data_id: str, file_path: str):
        if data_id in self._file_data.keys():
            raise Exception(f"The id '{data_id}' have existed, we can't save file")

        if not isfile(file_path):
            raise Exception(f"{file_path} is not a file")

        output_file = join(self._storage_folder, f"{str(uuid.uuid4())}")
        shutil.copy(src=file_path, dst=output_file)
        self._file_data[data_id] = {
            "original_file_name": basename(file_path),
            "stored_file": output_file
        }

    def load_file(self, data_id: str, target_path: str):
        stored_file = self._file_data[data_id]["stored_file"]
        shutil.copy(src=stored_file, dst=target_path)

    def destroy(self):
        for value in self._file_data.values():
            os.remove(value["stored_file"])

    def save_json(self, data_id: str, data: dict):
        self._json_data[data_id] = data

    def load_json(self, data_id: str) -> dict:
        return self._json_data[data_id]

    def save_string(self, data_id: str, data: str):
        self._str_data[data_id] = data

    def load_string(self, data_id: str) -> str:
        return self._str_data[data_id]
