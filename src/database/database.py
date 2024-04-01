import os
import pymongo 


client = pymongo.MongoClient(os.environ["MONGODB_URL"])
db = client.college
student_collection = db.get_collection("students")