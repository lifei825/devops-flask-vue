from utils.ext import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255), unique=True)
    outside = db.Column(db.String(255), unique=True)
    intranet = db.Column(db.String(255))
    idc = db.Column(db.String(255))
    area = db.Column(db.String(255))

    def to_json(self):
        doc = self.__dict__
        if "_sa_instance_state" in doc:
            del doc["_sa_instance_state"]

        if doc.get('confirmed_at', None):
            doc['confirmed_at'] = doc['confirmed_at'].strftime('%F %T')

        return doc
