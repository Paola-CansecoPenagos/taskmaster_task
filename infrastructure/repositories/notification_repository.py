from pymongo import MongoClient

class NotificationRepository:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db['notifications']
    
    def add_notification(self, notification):
        self.collection.insert_one(notification)
