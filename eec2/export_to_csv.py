# @Author: xiewenqian <int>
# @Date:   2016-11-28T20:35:09+08:00
# @Email:  wixb50@gmail.com
# @Last modified by:   int
# @Last modified time: 2016-12-01T19:32:48+08:00


import pandas as pd
from pymongo import MongoClient


def _connect_mongo():
    """ A util for making a connection to mongo """
    mongo_uri = "DATABASE-URL" # TODO - Replace DATABASE-URL with your mongodb database url
    conn = MongoClient(mongo_uri)
    return conn['eec2']


def export_mongo(collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    result = {'Email': [], 'Status': [], 'Participants Name': [], 'Participants Email': [],
              'Participants Phone Number': [],
              'Participants Age': [], 'Participants School': [], 'Participants Qualification': [],
              'Participants Address': [], 'Participants City': [], 'Participants Pin Code': []}
    # Connect to MongoDB
    db = _connect_mongo()

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    for x in cursor:
        email = name = age = address = city = school = phone = qualification = pin = ''
        result['Email'].append(x['_id'])
        if x['form_submitted']:
            result['Status'].append('Submitted')
        else:
            result['Status'].append('Not Submitted')
        if x['participant_1']:
            phone = str(x['participant_1']['phone_number'])
            name = str(x['participant_1']['full_name'])
            age = str(x['participant_1']['age'])
            email = str(x['participant_1']['email'])
            qualification = str(x['participant_1']['qualification'])
            address = str(x['participant_1']['address'])
            city = str(x['participant_1']['city'])
            pin = str(x['participant_1']['pin_code'])
            school = str(x['participant_1']['school'])
        if x['participant_2']:
            phone = '/'.join([phone, str(x['participant_2']['phone_number'])])
            name = '/'.join([name, str(x['participant_2']['full_name'])])
            age = '/'.join([age, str(x['participant_2']['age'])])
            email = '/'.join([email, str(x['participant_2']['email'])])
            qualification = '/'.join([qualification, str(x['participant_2']['qualification'])])
            address = '/'.join([address, str(x['participant_2']['address'])])
            city = '/'.join([city, str(x['participant_2']['city'])])
            pin = '/'.join([pin, str(x['participant_2']['pin_code'])])
            school = '/'.join([school, str(x['participant_2']['school'])])
        if x['participant_3']:
            phone = '/'.join([phone, str(x['participant_3']['phone_number'])])
            name = '/'.join([name, str(x['participant_3']['full_name'])])
            age = '/'.join([age, str(x['participant_3']['age'])])
            email = '/'.join([email, str(x['participant_3']['email'])])
            qualification = '/'.join([qualification, str(x['participant_3']['qualification'])])
            address = '/'.join([address, str(x['participant_3']['address'])])
            city = '/'.join([city, str(x['participant_3']['city'])])
            pin = '/'.join([pin, str(x['participant_3']['pin_code'])])
            school = '/'.join([school, str(x['participant_3']['school'])])
        if x['participant_4']:
            phone = '/'.join([phone, str(x['participant_4']['phone_number'])])
            name = '/'.join([name, str(x['participant_4']['full_name'])])
            age = '/'.join([age, str(x['participant_4']['age'])])
            email = '/'.join([email, str(x['participant_4']['email'])])
            qualification = '/'.join([qualification, str(x['participant_4']['qualification'])])
            address = '/'.join([address, str(x['participant_4']['address'])])
            city = '/'.join([city, str(x['participant_4']['city'])])
            pin = '/'.join([pin, str(x['participant_4']['pin_code'])])
            school = '/'.join([school, str(x['participant_4']['school'])])
        result['Participants Name'].append(name)
        result['Participants Qualification'].append(qualification)
        result['Participants Phone Number'].append(phone)
        result['Participants Pin Code'].append(pin)
        result['Participants Address'].append(address)
        result['Participants School'].append(school)
        result['Participants Email'].append(email)
        result['Participants City'].append(city)
        result['Participants Age'].append(age)

    df = pd.DataFrame(result, columns=['Email', 'Status', 'Participants Name', 'Participants Email',
                                       'Participants Phone Number',
                                       'Participants Age', 'Participants School', 'Participants Qualification',
                                       'Participants Address', 'Participants City', 'Participants Pin Code'])
    export_excel = df.to_excel(r'record.xlsx',
                               header=True)

    print(export_excel)


if __name__ == '__main__':
    export_mongo('users', {})
