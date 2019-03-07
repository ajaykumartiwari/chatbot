import nltk
import numpy as np
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "ChatBot Application"

if __name__ == '__main__':
    app.run()
