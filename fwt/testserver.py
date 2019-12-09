import csv
from datetime import datetime, timedelta, date
from random import randint
from fwt import app, db
from fwt.models import WeightRecord
import config

def fudge_db():
    with app.app_context():
        sw = 3466
        for i in range(364,0, -1):
            date = datetime.today().date() - timedelta(i)
            wr = WeightRecord(date, randint(sw-10,sw+10))
            db.session.add(wr)
            sw -= 1
        db.session.commit()

def fgfgd():
    with app.app_context():
        with open("gandiyaweightOct2016.csv", "rb") as data:
            reader = csv.reader(data)
            for day, weight in reader:
                print(day, weight)
                WeightRecord.query.all()
                y,m,d = day.split("-")
                wr = WeightRecord(date(int(y), int(m), int(d)), int(weight))
                db.session.add(wr)
            db.session.commit()

if __name__ == "__main__":
    app.config.from_object('config.Config')
    with app.app_context():
        db.create_all()
    fgfgd()
    app.run()


