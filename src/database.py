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

        self.colls = Collections()
        self.dbName = False
        self.is_connected = False

    def _get_database(self, dbname):
        if not self._is_mongodb_available():
            return False

        return self.client[dbname]

    def _is_mongodb_available(self):
        try:
            self.client = MongoClient(serverSelectionTimeoutMS=500)
            self.client.server_info()
        except:
            self.dbName = False
            return False

        if not self.dbName:
            return False

        return True


    def _get_collection(self, collname):
        if not self._is_mongodb_available():
            return False
        return self.db[collname]

    # -------------- BEG GENERALS
    def connect(self, databaseName):
        self.dbName = databaseName

        if not self._is_mongodb_available():
            return False

        self.db = self._get_database( self.dbName )
        return True

    def insert_element(self, collection, field):
        coll = self._get_collection(collection)
        if not coll: return False

        coll.insert(field)

    def delete_element(self, collection, query):
        coll = self._get_collection(collection)
        if not coll: return False

        coll.delete_one(query)

    # RET : number of updated field
    def update_field(self, collection, find_query, update_query):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.update(find_query, {"$set": update_query})["n"]

    # RET : number of updated field
    def push_item_to_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.update(find_query, {"$push": item})["n"]

    def pull_item_from_array(self, collection, find_query, item):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.update(find_query, {"$pull": item})["n"]

    # RET : first result of the query
    def query_result_single(self, collection, query):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.find_one(query)

    # RET : list of the result of the query
    def query_result_multi(self, collection, query):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.find(query)

    # RET : number of query result
    def count_query_result(self, collection, query):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.find(query).explain()["n"]

    def get_datetime(self):
        datetime_format = "%H:%M %d.%m.%y"
        return datetime.now().strftime(datetime_format)

    def str_to_datetime(self, str_dt):
        datetime_format = "%H:%M %d.%m.%y"
        return datetime.strptime(str_dt, datetime_format)

    # -------------- BEG MEMBER
    def add_new_member(self, firstname="", lastname="", email="", department="", mobilecyp="", mobileother=""):
        member = {
            "name": {"first": firstname, "last": lastname},
            "email": email,
            "department": department,
            "mobileNo": {"cyp": mobilecyp, "other": mobileother},
            "registration_date": self.get_datetime()
        }

        return self.insert_element(self.colls.member, member)

    def delete_member_by_email(self, email):
        query = {"email": email}
        return self.delete_element(self.colls.member, query)

    def total_num_of_members(self):
        return int(self.count_query_result(self.colls.member, {}))


def test():
    db = MongoDatabase()
    db.connect("FregTEST")
    db.add_new_member()


if __name__ == "__main__":
    test()
