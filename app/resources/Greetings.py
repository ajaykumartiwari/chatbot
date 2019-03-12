

import nltk
import warnings
import json
warnings.filterwarnings("ignore")
import csv
import numpy as np
import random
import string


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","how are you")
GREETING_RESPONSES = ["hi", "hey","Good Morning", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

# Checking for greetings
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)