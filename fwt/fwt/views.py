from __future__ import division
from fwt import app,db
from pygal import Line
from fwt.models import WeightRecord
from flask import render_template, request, redirect, flash, url_for
from datetime import datetime, timedelta,date
from bcrypt import hashpw
import re

hash = b"$2b$12$AQnQQAzuAD16NecZOdPPiOaRIFvd2Emw9eoZOxkcDSpjKCeo6Nye."
datefmt = re.compile(r'^\d{4}-\d\d-\d\d$')
weightfmt = re.compile(r'^\d\d\d(\.\d)?$')

@app.route('/')
def index():  
    CURRENT_WEIGHT = WeightRecord.query.all()[-1].weight/10
    START_WEIGHT = WeightRecord.query.all()[0].weight/10
    lost = START_WEIGHT - CURRENT_WEIGHT
    today = datetime.today().date().strftime("%Y-%m-%d")
    return render_template('index.html', title='Home', start_weight=START_WEIGHT, current_weight=CURRENT_WEIGHT, lost=lost, date=today)

@app.route('/log_weight', methods=['POST'])
def log_weight():
    password = request.form["password"].encode('utf-8')
    time = str(request.form["date"])
    weight = str(request.form["weight"])
    if hashpw(password, hash) == hash:
        if is_valid_date(time):
            if re.match(weightfmt, weight):
                y,m,d = time.split('-')
                wr = WeightRecord(date(int(y),int(m),int(d)), int(float(weight)*10))
                db.session.add(wr)
                db.session.commit()
            else:
                flash("Invalid date format. Date should be in format of YYYY-MM-DD")
        else:
            flash(u"Invalid Date. Date should be in the format of YYYY-MM-DD")
    else:
        flash(u'Incorrect Password')
    
    return redirect(url_for('index'))

@app.route('/charts/<time_range>.svg')
def line_route(time_range):
    #plots graphs for past 30 days
    if time_range == "past-30-days":
        start_day = datetime.today().date()- timedelta(30)
        chart = make_chart(start_day, "Weight For The Past 30 Days", 30)
    
    return chart.render_response()

def make_chart(start_date, title, plots=20):
    #takes start_date, end_date, plots
    #1. Create the series of days for the graph
    #2. Extract actual weight and averege weight and divide by 10
    #3. Chart with title, labels as days
    
    series = WeightRecord.query.filter(WeightRecord.date >= start_date).all()
    stagger = 1 if len(series) // plots == 0 else len(series) // plots
    series = [series[0]] + series[1:-1:stagger] + [series[-1]]
    weights = [rec.weight/10 for rec in series]
    av_weights = [rec.m_av/10 for rec in series]
    days = [rec.date for rec in series]

    chart = Line(title=title, x_label_rotation=45)
    chart.x_labels = days
    chart.add("Actual Weight", weights, stroke=False)
    chart.add("Average Weight", av_weights)
    
    return chart

def is_valid_date(datestr):
    return re.search(datefmt, datestr)

