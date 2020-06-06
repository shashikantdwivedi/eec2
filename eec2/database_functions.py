import db
import random
import json


def mail_username():
    mail = db.admin.find_one({"_id": "email_configuration"})
    return mail["mail_username"]


def mail_password():
    mail = db.admin.find_one({"_id": "email_configuration"})
    return mail["mail_password"]


def add_new_user(user_info):
    result = db.users.find()
    if result:
        for x in result:
            if user_info["_id"] == x["_id"]:
                return False
        user_info["otp"] = random.randint(999, 9999)
        user_info["account_validity"] = 1
        user_info["form_uploaded"] = 0
        user_info["participant_1"] = 0
        user_info["participant_2"] = 0
        user_info["participant_3"] = 0
        user_info["participant_4"] = 0
        user_info["form_submitted"] = 0
        db.users.insert_one(user_info)
        return True


def verify_otp(email, otp):
    user = db.users.find_one({"_id": email})
    if user["otp"] == otp:
        db.users.update_one({"_id": email}, {"$set": {"otp": random.randint(999, 9999), "account_validity": 1}})
        return True
    else:
        return False


def validate_login(email, password):
    result = db.users.find_one({'_id': email, 'password': password})
    if result:
        return result
    else:
        return 0


def get_otp(email):
    result = db.users.find_one({"_id": email})
    return result["otp"]


def form_uploaded(email):
    db.users.update_one({"_id": email}, {"$set": {"form_uploaded": 1}})


def form_status(email):
    result = db.users.find_one({"_id": email})
    return result['form_uploaded']


def register_participant(email, user_number, participant_data):
    result = db.users.find_one({"_id": email})
    participant = 'participant_' + str(user_number)
    if not result[participant]:
        db.users.update_one({"_id": email}, {"$set": {participant: participant_data}})
        return True
    else:
        return False


def export_json(email):
    result = db.users.find_one({"_id": email})
    return result


def verify_upload(email):
    result = db.users.find_one({"_id": email})
    if result["form_uploaded"]:
        return True
    else:
        return False


def form_upload_done(email):
    db.users.update_one({"_id": email}, {"$set": {"form_submitted": 1}})


def verify_submission(email):
    result = db.users.find_one({"_id": email})
    if result["form_submitted"]:
        return True
    else:
        return False


def verify_participants(email):
    result = db.users.find_one({"_id": email})
    if result['participant_1'] or result['participant_2'] or result['participant_3'] or result['participant_4']:
        return True
    else:
        return False


def registration_status(email):
    result = db.users.find_one({"_id": email})
    if result['form_submitted']:
        return True
    else:
        return False

