
import csv
import json
import random
import string
import warnings
import pandas as pd 
import os
import matplotlib.pyplot as plt
import requests
import re

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
# from chatterbot import ChatBot
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
    # patter to validate mobile number
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}")

    print("Mehtod begining")
    data = request.get_json()
    message = data['message']
    print("Message ===========> ", message)

    user_response = tokenized_user_request(message)
    user_res = str(user_response)

    # mobile number validation
    print("Pattern.match(user_res)- ",Pattern.match(user_res)," len(user_res)- ",len(user_res) == 10, " user_res.isdigit()",user_res.isdigit())
    if(len(user_res) == 10 and user_res.isdigit()):
        print("valid mobile number")
        resposne = getOtp(user_res)
        otpFlag = True
        global validMobileNumber 
        validMobileNumber = user_res
        if(response is None ):
            return jsonResponse(resposne)
        else:
           return jsonResponse("valid number")

    # Otp validation
    if(len(user_res) == 4 and user_res.isdigit()):
        if(user_res == "1111"):
            print("valid otp number")
            print("validMobileNumber  -> ",validMobileNumber)
            # varifyOtp(user_res)
            accountDetailsData = accountDetails()
            print("response to ui accountDetailsData-->",accountDetailsData,"  ",type(accountDetailsData))
            return jsonify({'result': accountDetailsData, 'message': "account details"})
        else :
            return jsonResponse("inValid otp")


    if(user_response == 'account' or user_response == 'balance' or user_response == 'show my balance' or user_response == 'summary' or user_response == 'show account balance' or user_response == 'display account balance' or user_response == 'account balance' or user_response == 'login' or user_response == 'show balance' or user_response == 'display balance' or user_response == 'want login'):
       return jsonResponse("login modal")

    if(user_response == 'update' or user_response == 'updateaddress' or user_response == 'displayaddress' or user_response == 'editaddress' or user_response == 'address' or user_response == 'edit'):
        #updateUser = getUserAddress(uname)
        return jsonResponse("update modal")

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
    data = pd.read_csv('D:\Erste POC\chatbot_improvemnt\Data.csv')
    login_data = request.get_json()
    uname = login_data['username']
    passw = login_data['password'] 

    for index, row in data.iterrows():
        print("Matching Row Data =============>",row)
        if(row['Login ID'] == uname and row['Password'] == passw):
            status=True
            print("Matching Row Data successfully...")
            #f= open("D:\chatbot_file\chat.txt","w+")
            #f= open(r'\\BLR26014TEAM1\Erste\chat.txt',"w+")
            user_input = json.dumps(login_data)
            uname = row['Login ID']
            passw = row['Password']    
       
            print("Login Data =======================> ", uname, passw)
            session['logged_in'] = True
            print("Session Data======>",session)
            
            # External Api Call and Display account data from Data.csv file when login successfull
            userdata = {'userId': row['Login ID'], 'id': row['Account Number'], 'name': row['Acc Holder Name'], 'balance': row['Account Balance']}
            print("User Details =============>",userdata)
            return jsonify({'result': userdata},)
    else:
        status = False
        return jsonResponse("Invalid User")
def accountDetails():
    data = pd.read_csv('D:\Erste POC\chatbot_improvemnt\Data.csv')

    for index, row in data.iterrows():
        if(str(row['Mobile Number']) == validMobileNumber):
            status=True
            print("Matching Row Data successfully...")
            session['logged_in'] = True
            # External Api Call and Display account data from Data.csv file when login successfull
            userdata = {'userId': row['Login ID'], 'id': row['Account Number'], 'name': row['Acc Holder Name'], 'balance': row['Account Balance']}
            print("User Details =============>",userdata)
            return userdata


# @app.route('/getOtp', methods=['POST'])
def getOtp(user_res):
    #loc = pd.read_csv("userdata.xlsx") 
    
    print("======================================================>>>>>>>>>>>>>>>>>>>>")
    data = pd.read_csv('D:\Erste POC\chatbot_improvemnt\Otp_validation_01.csv')
    # user_otp_data = request.get_json()
    print("user_res in getOtop()-- ",user_res)
    user_otp_data = user_res
    mobileNumber = user_otp_data
    
    for index, row in data.iterrows():
        if(str(row['Mobile Number']) == mobileNumber):
            status=True
            print("inside if Matching Row Data found successfully...")
            user_input = json.dumps(user_otp_data)

            mobileNumber = str(row['Mobile Number'])
            otp = str(row['OTP'])
            session['logged_in'] = True
            print("Session Data======>",session)
            
            # External Api Call and Display account data from Data.csv file when login successfull
            otpDataRto = {'mobileNumber': mobileNumber, 'otpNumber': otp}
            # userdata = {'userId': uname, 'id': row['Account Number'], 'name': row['Acc Holder Name'], 'balance': row['Account Balance']}
            print("otp Details =============>",otpDataRto)
            return jsonify({'result': otpDataRto},)
    else:
        status = False
        return jsonResponse("Mobile number is not registered,Please entyer registered mobile number ")

@app.route('/varifyOtp',methods = ['POST', 'GET'])
def varifyOtp(user_res):
    print("======================================================>>>>>>>>>>>>>>>>>>>>")
    data = pd.read_csv('D:\Erste POC\chatbot_improvemnt\Otp_validation_01.csv')
    # user_otp_data = request.get_json()
    print("user_res in getOtop()-- ",user_res)
    user_otp_data = user_res

    mobileNumber = validMobileNumber
    print("validMobileNumber -> ",validMobileNumber)

    for index, row in data.iterrows():
        if(str(row['Mobile Number']) == mobileNumber):
            status=True
            print("inside if Matching Row Data found successfully...")
            user_input = json.dumps(user_otp_data)

            if(str(user_otp_data) == str(row['OTP'])):
                mobileNumber = str(row['Mobile Number'])
                otp = str(row['OTP'])
                print("OTP Data =======================> ", mobileNumber, otp)

           

            session['logged_in'] = True
            print("Session Data======>",session)
            
            # External Api Call and Display account data from Data.csv file when login successfull
            otpDataRto = {'mobileNumber': mobileNumber, 'otpNumber': otp}
            # userdata = {'userId': uname, 'id': row['Account Number'], 'name': row['Acc Holder Name'], 'balance': row['Account Balance']}
            print("otp Details =============>",otpDataRto)
            return jsonify({'result': otpDataRto},)
    else:
        status = False
        return jsonResponse("invalid otp ")



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

    with open('Customer_Details.csv', mode='w') as csv_file:
    #with open(r'\\BLR26014TEAM1\Erste\Customer_Details.csv', "w+") as csv_file:
        fieldnames = ['userId', 'name', 'addressLine1','addressLine2','city','state','country','zipcode']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        #{'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'}
        writer.writerow(data)

    #======================= Fetching Updeted User Address Details =============================#
    data = pd.read_csv('Customer_details.csv')
    #data = pd.read_csv(r'\\BLR26014TEAM1\Erste\Customer_details.csv')
    
    for index, row in data.iterrows():
        print("Matching Row Data =============>",row)
        if(userId == row['userId']):
            print("Matching  =============>",row)
            userUpdatedAddress = {'id': row['userId'], 'name': row['name'], 'addressLine1': row['addressLine1'],'addressLine2': row['addressLine2'],
            'city': row['city'], 'state': row['state'], 'country': row['country'], 'zipcode': row['zipcode']}
            #f= open(r'\\BLR26014TEAM1\Erste\address.txt',"w+")
            f= open(r'D:\chatbot_file\address.txt',"w+")
            add1 = userUpdatedAddress['addressLine1']
            add2 = userUpdatedAddress['addressLine2']
            city = userUpdatedAddress['city']
            state = userUpdatedAddress['state']
            country = userUpdatedAddress['country']
            zipcode = userUpdatedAddress['zipcode']
            if(userUpdatedAddress != ''):      
                f.write(str(add1) +","+ str(add2) +","+str(city) +","+str(state) +","+str(country) +","+str(zipcode))
            print("Updated Data=========>", row)
            return jsonify({'result': userUpdatedAddress},)

# @app.route('/getUser',methods = ['POST', 'GET'])
# def getUserAddress(uname):
#     data = pd.read_csv('Customer_details.csv')
    
#     for index, row in data.iterrows():
#         print("Matching Row Data =============>",row)
#         if(uname == row['userId']):
#             print("Matching  =============>",row)
#             userAddress = {'id': uname, 'name': row['name'], 'addressLine1': row['addressLine1'],'addressLine1': row['addressLine1'],
#             'city': row['city'], 'state': row['state'], 'country': row['country'], 'zipcode': row['zipcode']}
#             print("User Details =============>",userdata)
#             # ===========================================
#             return userAddress

@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='localhost')
#app.run(host='10.6.184.194')








