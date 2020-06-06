import db


if __name__ == "__main__":
    # TODO - Replace the EMAIL-ID and EMAIL-PASSWORD with the right values.
    info = {
        "_id": "email_configuration",
        "mail_username": "EMAIL-ID",
        "mail_password": "EMAIL-PASSWORD",
    }

    db.admin.insert_one(info)
