from flask import Flask, render_template
from modules import convert_to_dict, make_ordinal
import pandas as pd

app = Flask(__name__)
application = app

#Sample of User Data Over Past 100 Days
user_test = pd.read_csv('TEST_USER_DATA.csv')
user_test
