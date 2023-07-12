from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transfer(db.Model):
    transferId = db.Column(db.Integer, primary_key = True)
    sendAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    receiveAccId = db.Column(db.Integer, db.ForeignKey("acc.accId"), nullable = False)
    transferAmt = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String, nullable = False)
    sendAcc = db.relationship("Acc", backref = db.backref("outgoing", lazy = True))
    receiveAcc = db.relationship("Acc", backref = db.backref("incoming"), lazy = True)