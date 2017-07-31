# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime


class MongoDatabase:
    # -------------- BEG PRIVATE
    def __init__(self):
        # self._connect()
        # self.db = self._get_database("Freg_test")
        # Collections class It just stores collection names
        class Collections:
            def __init__(self):
                #  if you have new collection, put it here as below
                self.member = "Member"
                self.department = "Department"

        self.colls = Collections()
        self.dbName = ""

    def _connect(self, databaseName):
        self.dbName = databaseName
        try:
            self.client = MongoClient()
            self.db = self._get_database(self.dbName)
            return True
        except:
            return False

    def _get_database(self, dbname):
        return self.client[dbname]

    def _get_collection(self, collname):
        return self.db[collname]

    # -------------- BEG GENERALS
    def insert_element(self, collection, field):
        coll = self._get_collection(collection)
        coll.insert(field)

    # RET : number of updated field
    def update_field(self, collection, find_query, update_query):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$set": update_query})["n"]

    # RET : number of updated field
    def push_item_to_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$push": item})["n"]

    def pull_item_from_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        return coll.update(find_query, {"$pull": item})["n"]

    # RET : first result of the query
    def query_result_single(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find_one(query)

    # RET : list of the result of the query
    def query_result_multi(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find(query)

    # RET : number of query result
    def count_query_result(self, collection, query):
        coll = self._get_collection(collection)
        return coll.find(query).explain()["n"]

    def get_datetime(self):
        datetime_format = "%H:%M %d.%m.%y"
        return datetime.now().strftime(datetime_format)

    def str_to_datetime(self, str_dt):
        datetime_format = "%H:%M %d.%m.%y"
        return datetime.strptime(str_dt, datetime_format)

    # -------------- BEG MEMBER
    def add_new_member(self, firstname="", lastname="", email="", department="", mobilencc="", mobiletr=""):
        member = {
            "first_name": firstname,
            "last_name": lastname,
            "email": email,
            "department": department,
            "mobile_ncc": mobilencc,
            "mobile_tr": mobiletr,
            "registration_date": self.get_datetime()
        }

        self.insert_element(self.colls.member, member)

    def delete_member_by_email(self, email):
        pass  # TODO
