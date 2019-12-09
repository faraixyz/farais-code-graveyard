from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime

db = SQLAlchemy()
MOVING_AVERAGE_STEPS = 10

class WeightRecord(db.Model):
    """
    Defining the model to keep weight records consisting
    of Weight in tenths of pounds and Date in the fomrat
    YYYY-MM-DD
    """
    __tablename__ = "WeightRecords"
    date = db.Column(db.Date, primary_key=True)
    weight = db.Column(db.Integer)
    m_av = db.Column(db.Integer)

    def __init__(self, date, weight):
        self.date = date
        self.weight = weight
        self.m_av = self.calculate_moving_average()
    
    def __repr__(self):
        return "<Date:%s Weight:%sdlbs Average:%sdlbs" % (self.date, self.weight, self.m_av)
    
    def calculate_moving_average(self):
        rec_count = self.query.count()
        yest = self.date - timedelta(1)

        if rec_count < MOVING_AVERAGE_STEPS+1:
            if rec_count == 0:
                return self.weight
            else:
                prev_rec = self.query.filter(WeightRecord.date == yest).first()
                m_av = ((prev_rec.m_av * rec_count) + self.weight) / (rec_count + 1)
        else:
            prev_rec = self.query.filter(WeightRecord.date == yest).first()
            m_av = (prev_rec.m_av * (MOVING_AVERAGE_STEPS-1) + self.weight) / MOVING_AVERAGE_STEPS

        return int(m_av)
    
    def get_start_weight(self):
        return WeightRecord.query.all()[0]
    
    def get_current_weight(self):
        return WeightRecord.query.all()[-1]
