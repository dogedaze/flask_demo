from logging import info
from flask import render_template, flash, redirect, url_for,request,jsonify
from app import app
from app.forms import LoginForm
import pandas as pd
from pandas import DataFrame, read_csv
from wtforms import StringField, SubmitField,Form
from wtforms.validators import DataRequired
import json
import plotly
import plotly.express as px
import yfinance as yf
import random


@app.route('/home')
def home():
    user = {'username': 'Viktor'}
    posts = [
        {
            'author': {'username': 'John Quixote | John'},
            'body': 'I hate this ETF!'
        },
        {
            'author': {'username': 'FAANG girl | Susan'},
            'body': 'This is a for sure invest!'
        }
    ]
    return render_template('home.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)


@app.route("/view", methods=("POST", "GET"))
def html_table():
    df = pd.read_csv('df_balance_user_1.csv')
    return render_template('view.html',  tables=[df.to_html(classes='table table-striped table-bordered table-hover table-sm', header="true")])

@app.route("/view/1", methods=("POST", "GET"))
def html_table_user1():
    df = pd.read_csv('df_trades_user_1.csv')
    return render_template('view.html',  tables=[df.to_html(classes='table table-striped table-bordered table-hover table-sm', header="true")])
@app.route("/view/2", methods=("POST", "GET"))
def html_table_user2():
    df = pd.read_csv('df_trades_user_2.csv')
    return render_template('view2.html',  tables=[df.to_html(classes='table table-striped table-bordered table-hover table-sm', header="true")])

@app.route('/view/<name>')
def user(name):
    return render_template('view_U.html', name=name)

@app.route("/LEADER", methods=("POST", "GET"))
def html_table1():
    df = pd.read_csv('df_final_portfolio_amount.csv',index_col=False) 
    return render_template('view.html',  tables=[df.to_html(classes='table table-striped table-bordered table-hover table-sm', header="true")])


@app.route("/matchup", methods=("POST", "GET"))
def html_table2():
    df = pd.read_csv('app/remaining.csv',index_col=False) 
    return render_template('match.html',  tables=[df.to_html(classes='table table-striped table-bordered table-hover table-sm', header="true")])

@app.route("/embeds", methods=("POST", "GET"))
def embeds():
    urls = [
        'https://drive.google.com/file/d/1iz3mwdGgU-XQ0i5_ZEhzVwXvF0bO_GV7/view?usp=sharing'
     
    ]

    iframe = random.choice(urls)

    return render_template('iframes.html', iframe=iframe)

@app.route('/')
def index():

    user = {'username': 'Viktor'}
    posts = [
        {
            'author': {'username': 'John Quixote | John'},
            'body': 'Teach me your ways!'
        },
        {
            'author': {'username': 'FAANG girl | Susan'},
            'body': 'I will beat you this week.'
        }
    ]
    return render_template('stock2.html',title='Home', user=user, posts=posts)

@app.route('/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('data'),request.args.get('period'),request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(stock,period, interval):
    st = yf.Ticker(stock)
  
    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df=df.reset_index()
    df.columns = ['Date-Time']+list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )


    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

