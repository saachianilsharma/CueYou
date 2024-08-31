from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from datetime import datetime


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

def add_user(name, email, password, country, field_of_work, position, experience, is_student, usage_purpose):
    """
    Add a new user to the Userdir collection with an auto-incremented userid.
    """
    if user_collection.find_one({"emailid": email}):
        return "Email already registered with us"

    userid = str(get_next_userid())
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_user = {
        "userid": userid,
        "emailid": email,
        "name": name,
        "password": hashed_password,  # Make sure to hash the password before storing it
        "country": country,
        "field_of_work": field_of_work,
        "position": position,
        "experience": experience,
        "is_student": is_student,
        "usage_purpose": usage_purpose,
        "created_at": datetime.now(),
        "session_token": None  # Initialize with no active session
    }

    try:
        user_collection.insert_one(new_user)
        return "Account created successfully"
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

def get_otp(userid):
    #return otp_collection.find_one({'Userid': userid})
    # Find the document in otp_collection where 'Userid' matches the provided userid
    user_otp_data = otp_collection.find_one({'Userid': userid})
    
    # Check if the document was found and if it contains the 'OTP' field
    if user_otp_data and 'OTP' in user_otp_data:
        return user_otp_data['OTP']  # Return only the OTP value
    
    return None  

def delete_otp(userid):
    otp_collection.delete_one({'Userid': userid})

def update_password(userid, new_password):
    user_collection.update_one({'userid': userid}, {'$set': {'password': new_password}})

def update_session_token(user_id, session_token):
    """
    Updates the session token for the specified user in the MongoDB collection.
    
    Args:
        user_id (str): The unique identifier of the user.
        session_token (str): The new session token to be saved in the database.
    """
    try:
        # Update the session_token field in the user's record
        result = user_collection.update_one(
            {"userid": str(user_id)}, 
            {"$set": {"session_token": session_token}}
        )

        # Check if the update was successful
        if result.matched_count > 0:
            print("Session token updated successfully.")
        else:
            print("No matching user found. Session token update failed.")
    
    except Exception as e:
        print(f"Error updating session token: {e}")

def clear_session_token(session_token):
    """
    Clears the session token in the database when the user logs out.
    
    Args:
        session_token (str): The session token to be cleared.
    """
    try:
        result = user_collection.update_one(
            {"session_token": session_token},
            {"$unset": {"session_token": ""}}
        )
        if result.matched_count > 0:
            print("Session token cleared successfully.")
        else:
            print("No matching session found. Token clearance failed.")
    except Exception as e:
        print(f"Error clearing session token: {e}")

def get_user_by_token(session_token):
    """
    Retrieves the user from the database based on the session token.
    
    Args:
        session_token (str): The session token used to fetch the user record.
        
    Returns:
        dict: User record if found, else None.
    """
    try:
        print("type of token= ",type(session_token))
        print("Value of token:", session_token)
        user = user_collection.find_one({"session_token": str(session_token)})
        print ("Retrieved user:",user)
        return user
    except Exception as e:
        print(f"Error retrieving user by session token: {e}")
        return None
