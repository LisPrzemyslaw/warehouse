from __future__ import annotations

import os
import json

import pymongo


class DataBase:
    __instance: DataBase = None

    # TODO it should be secured :)
    API = "mongodb://nierelacyjne-bazy-danych:n1Vyz2NMj7tLU6poJNgHQd1bNbaty0pOSQi0BXUayQ5oKlrtLjFva8gmgUYDzhCvhA4Pi2uKfSBtACDbxCy7UQ==@nierelacyjne-bazy-danych.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@nierelacyjne-bazy-danych@"

    def __new__(cls, *args, **kwargs):
        if DataBase.__instance is None:
            DataBase.__instance = object.__new__(cls)
            DataBase.initialized = None
        return DataBase.__instance

    def __init__(self):
        if self.initialized is None:
            self.client = pymongo.MongoClient(DataBase.API)
            self.database = self.client["nierelacyjne-bazy-danych"]
            self.collections = self.database.list_collections()

            # to keep as singleton
            self.initialized = True

    def insert(self, collection: str, data: dict) -> str:
        inserted_id = self.database[collection].insert_one(data).inserted_id
        print(f"inserted uniq _id: {inserted_id}")
        return inserted_id

    def delete_docs_from_collection(self, collection: str, filter=None):
        """ This function will delete all files from collection"""
        if filter is None:
            filter = {}
        self.database[collection].delete_many(filter)

    def save_data_to_json_file(self, collection, file_name, filter=None):
        """
        This function save collection to json file / files. If there is more than one file to save.
        In function there is validation that can update file_name to correct format with .json extension
        """
        if filter is None:
            filter = {}

        # validate file_name
        path = file_name.split(".")
        file_name = path[0]
        if os.path.isabs(file_name):
            abs_path = file_name
        else:
            abs_path = os.path.join(os.getcwd(), file_name)

        all_datas_to_save = self.database[collection].find(filter)
        for data in all_datas_to_save:
            data["_id"] = str(data["_id"])
            with open(f"{abs_path}_{data['_id']}.json", "w") as out_file:
                json.dump(data, out_file)

    def read_from_file(self, file_name: str):
        if not file_name.endswith(".json"):
            file_name += ".json"

        if os.path.isabs(file_name):
            abs_file = file_name
        else:
            abs_file = os.path.join(os.getcwd(), file_name)

        if not os.path.exists(abs_file):
            raise FileNotFoundError(f"File: {abs_file} is not correct, change file_name!")

        with open(abs_file, "r") as file:
            return json.load(file)


if __name__ == '__main__':
    pass
