# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime
import logging

# BEG LOGGING
# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='freg.log',
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)


# END LOGGING

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

    def is_mongodb_available(self):
        logger.info("--> is_mongodb_available checking...")
        try:
            self.client = MongoClient(serverSelectionTimeoutMS=500)
            self.client.server_info()
        except Exception as e:
            logger.error("<-- is_mongodb_available error check :\n" + e)
            self.is_connected = False
            return False

        self.is_connected = True
        logger.info("<-- is_mongodb_available is OK. Return True.")
        return True

    def _get_database(self, dbname):
        return self.client[dbname]

    def _get_collection(self, collname):
        if not self.is_mongodb_available():
            logger.info("Couldn't get the " + collname + " collection. Return False.")
            return False
        return self.db[collname]

    # -------------- BEG GENERALS
    def connect(self, dbName="Test"):
        logger.info("--> MongoDatabase.connect dbName:" + dbName)
        if not self.is_mongodb_available():
            return False

        self.dbName = dbName
        self.db = self._get_database(self.dbName)

        logger.info("<-- MongoDatabase.connect is OK. Return True.")
        return True

    def insert_element(self, collection, field):
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.insert(field)

    def delete_element(self, collection, query):
        logger.info("delete_element collection:" + collection + " query:" + str(query))
        coll = self._get_collection(collection)
        if not coll: return False

        return coll.delete_one(query)

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
        logger.info("query_result_multi collection:" + collection + " query:" + str(query))
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
        logger.info("--> add_new_member email:" + email)
        member = {
            "name": {"first": firstname, "last": lastname},
            "email": {"metu": "", "other": email},
            "department": {"name": department},
            "mobileNo": {"cyp": mobilecyp, "other": mobileother},
            "registration_date": self.get_datetime()
        }

        if self.insert_element(self.colls.member, member) is False:
            logger.info("<-- add_new_member email:" + email + " couldn't added to db. Return False")
            return False

        logger.info("<-- add_new_member email:" + email + " is OK. Return True")
        return True

    def delete_member_by_email(self, email):
        logger.info("--> delete_member_by_email email:" + email)
        query = {"email.other": email}

        if self.delete_element(self.colls.member, query) is False:
            logger.info("<-- delete_member_by_email email:" + email + " No member is deleted.")
            return False

        logger.info("<-- delete_member_by_email email:" + email + " Member is deleted.")
        return True

    def total_num_of_members(self):
        return int(self.count_query_result(self.colls.member, {}))


def test():
    db = MongoDatabase()
    db.connect("Freg_test")

    print(db.delete_member_by_email("49@gmail.com"))
    # db.add_new_member()


if __name__ == "__main__":
    test()
    pass
