import csv
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fwt.models import WeightRecord

engine = create_engine('postgresql://localhost/fwt')
Session = sessionmaker(bind=engine)
session = Session()

with open("gandiyaweightOct2016.csv", 'rb') as data:
    reader = csv.reader(data)
    for day,weight in reader:
        y,m,d = day.split('-')
        wr = WeightRecord(date(int(y), int(m), int(d)), int(weight))
        session.add(wr)
    session.commit()
