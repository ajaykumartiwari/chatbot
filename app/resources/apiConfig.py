import requests

import nltk
import numpy as np
from flask import Flask, jsonify, redirect, request, url_for, session
from flask_restful import Api, Resource



def config():
    resp = requests.get('http://dummy.restapiexample.com/api/v1/employees')
    if resp.status_code != 200:
    # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for todo_item in resp.json():
       #userdata = '{} {} {}'.format(todo_item['id'], todo_item['employee_name'], todo_item['employee_salary'])
       userdata = {'id': todo_item['id'], 'name': todo_item['employee_name'], 'salary': todo_item['employee_salary']}
    print("User Data ======>",userdata)
    return userdata
    #print('{} {}'.format(todo_item['id'], todo_item['employee_name']))
    #output = {'first_name': new_customer['first_name'], 'last_name': new_customer['last_name']}


def update():
    updateUser = {'userId': "100",
     'name': "Ajay Tiwari",
     'addline1': "PaiLayout",
     'addLine2': "Tin factory",
     'city': "bangalore",
     'state': "Karnataka",
     'country': "India",
     'zipcode': 560016
    }
    return updateUser