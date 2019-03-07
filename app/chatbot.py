
import csv
import json
import random
import string
import warnings

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
# from resources.ChatbotImpl import response
from resources.botImpl import response

""" Mongodb Connection File """
#from DbConfig.connection import getAllRecords
from chatterbot import ChatBot
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Set secret access key
#app.secret_key = os.urandom(24)

CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/chatbot',methods = ['POST', 'GET'])
@cross_origin(origin='*')
def chatbot():
    print("Mehtod begining")
    data = request.get_json()
    message = data['message']
    print("Message ===========> ", message)

    user_response = tokenized_user_request(message)

    if(user_response == 'account'):
        return jsonResponse("login")

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


if __name__ == '__main__':
    app.run()
