
import csv
import json
import random
import string
import warnings
import pandas as pd 
import os
import matplotlib.pyplot as plt
import requests

import nltk
import numpy as np
from flask import Flask, jsonify, redirect, request, url_for, session
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin  # Access Cross origin from angular

# Remove stopwords like a, as ,are, we
from nltk.corpus import stopwords
stopwords.words('english')

from resources.Greetings import greeting
from resources.stopwords import tokenized_user_request
from resources.apiConfig import config, update
# from resources.ChatbotImpl import response
from resources.botImpl import response

""" Mongodb Connection File """
#from DbConfig.connection import getAllRecords
from chatterbot import ChatBot
warnings.filterwarnings("ignore")
plt.figure(figsize=(30, 20))

app = Flask(__name__)

# Set secret access key
app.secret_key = os.urandom(24)
access_token = app.secret_key
print("Secret key ==============>", access_token)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
@cross_origin(origin='*')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/chatbot',methods = ['POST', 'GET'])
def chatbot():
    
    print("Mehtod begining")
    data = request.get_json()
    message = data['message']
    print("Message ===========> ", message)

    user_response = tokenized_user_request(message)

    if(user_response == 'account' or user_response == 'balance' or user_response == 'summary' or user_response == 'showaccountbalance' or user_response == 'displayaccountbalance' or user_response == 'accountbalance' or user_response == 'login'):
        return jsonResponse("login")

    if(user_response == 'update'):
        return jsonResponse("update")

    #print("Final data ========= >",user_response)

    flag = True
    while(flag==True):
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you'):
                flag=False
                print("ROBO: You are welcome..")
                return jsonResponse(user_response)
            else:
                if(greeting(user_response)!=None):
                    print("ROBO: "+greeting(user_response))
                    # res = connect(user_response)
                    # print("Db Response ",res['answer'])
                    # answer = res['answer']
                    return jsonResponse(greeting(user_response))
                else:
                    print("ROBO: ",end="")
                    return jsonResponse(response(user_response))
                    
        else:
            flag=False
            print("ROBO: Bye! take care..")

# Convert String into JSON format
def jsonResponse(user_request):
    return jsonify(message=user_request)


@app.route('/login', methods=['POST'])
def login():
    
    #loc = pd.read_csv("userdata.xlsx") 
    print("======================================================>>>>>>>>>>>>>>>>>>>>")
    data = pd.read_csv('D:\chatbot_file\Data.csv')

    # username = data['Login ID'].values
    # password = data['Password'].values
    
    #pas = ''.join(map(str, password))
    #print("printing data===>",username, type(pas),pas)
    login_data = request.get_json()
    uname = login_data['username']
    passw = login_data['password'] 

    for index, row in data.iterrows():
        print("Matching Row Data =============>",row)
        if(row['Login ID'] == uname and row['Password'] == passw):
            print("Matching Row Data =============>",row)
            f= open("D:\chatbot_file\chat.txt","w+")
            user_input = json.dumps(login_data)
            if(user_input != ''):
                f.write(user_input)
            #f= open("\\BLR26014TEAM1\\Erste\\test.txt","w+")
            f.close()
            print("Login Data =======================> ", uname, passw)
            session['logged_in'] = True
            print("Session Data======>",session)
            
            # External Api Call and Accound Data display 
            # print(config())
            #userdata = config()
            userdata = {'id': row['Account Number'], 'name': row['Acc Holder Name'], 'balance': row['Account Balance']}
            print("User Details =============>",userdata)

            # ===========================================
            status = True
            return jsonify({'result': userdata},)
        # else:
        #     status = False
        #     return jsonResponse("Invalid Credentials! please try again")
    else:
        status = False
        return jsonResponse("Invalid Credentials! please try again")

@app.route('/update', methods=['GET','POST','PUT'])
def update():

    print("Inside Update Method")
    data = request.get_json()
    print("Update Data ============ >", data, type(data))
    userId = data['userId']
    name = data['name']
    addressLine1 = data['addressLine1']
    addressLine2 = data['addressLine2']
    city = data['city']
    state = data['state']
    country = data['country']
    zipcode = data['zipcode']

    #udf = pd.DataFrame([data])

    #writer = pd.ExcelWriter('customer_details.xlsx', engine='xlsxwriter')
    # udf.to_excel(writer, sheet_name='Customer Details')
    # writer.save()

    with open('Customer_Details.csv', mode='w') as csv_file:
        fieldnames = ['userId', 'name', 'addressLine1','addressLine2','city','state','country','zipcode']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        #{'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'}
        writer.writerow(data)

    # updateUser = update()
    print("Update Data=========>", data)
    return jsonify("User Update Successfully!")
    # json_data = request.json
    # user = User.query.filter_by(username=json_data['username']).first()
    # if user and bcrypt.check_password_hash(
    #         user.password, json_data['password']):
    #     session['logged_in'] = True
    #     status = True
    # else:
    #     status = False
    # return jsonify({'result': status})

@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run()









