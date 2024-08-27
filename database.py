from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib


client = MongoClient('mongodb://localhost:27017/')
db = client['CUEDB']
user_collection = db['userdir']
otp_collection = db['tempotp']

def get_next_userid():
    """
    Get the next userid by finding the maximum userid and incrementing it by 1.
    """
    last_user = user_collection.find_one(sort=[("userid", -1)])
    if last_user:
        return int(last_user['userid']) + 1
    else:
        return 1  # Start from 1 if no users exist

def add_user(name, email, password):
    """
    Add a new user to the Userdir collection with an auto-incremented userid.
    """
    if user_collection.find_one({"emailid": email}):
        return "email already registered with us"

    userid = str(get_next_userid())
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = {
        "userid": userid,
        "emailid": email,
        "name": name,
        "password": hashed_password  # Make sure to hash the password before storing it
    }

    try:
        user_collection.insert_one(new_user)
        return "account created successfully"
    except Exception as e:
        return str(e)


def get_user(email, password):
    #hashed_password=hashlib.sha256(password.encode()).hexdigest()
    #print(user_collection.find_one({'emailid': email, 'password': hashed_password}))
    #return user_collection.find_one({'emailid': email, 'password': hashed_password})
    print(email)
    user = user_collection.find_one({'emailid': email})
    print(user)
    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(hashed_password)
        if user['password'] == hashed_password:
            return user
    return None

def get_user_by_email(email):
    return user_collection.find_one({'emailid': email})

def add_otp(userid, otp):
    otp_collection.insert_one({'Userid': userid, 'OTP': otp})

def get_otp(userid, otp):
    return otp_collection.find_one({'Userid': userid, 'OTP': otp})

def delete_otp(userid):
    otp_collection.delete_one({'Userid': userid})

def update_password(userid, new_password):
    user_collection.update_one({'userid': userid}, {'$set': {'password': new_password}})
