from flask import Flask, logging
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import datetime
from web import app

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    billing_address = db.Column(db.String(255))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    email = db.Column(db.String(120))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(120))

    def __init__(self, email, first_name, last_name, billing_address, city, state, zip_code, country='US'):
        self.first_name = first_name
        self.email = email
        self.last_name = last_name
        self.billing_address = billing_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def __repr__(self):
        return '<User %r>' % self.first_name + " " + self.last_name

    def create_order(self, stripe_transaction, amount, name, description, recurring, sales_type):
        """

        :rtype : object
        """
        transaction_obj = Transaction(name, description, stripe_transaction, amount, recurring, sales_type,self.id)
        db.session.add(transaction_obj)
        return db.session.commit()

    def add_stripe_source(self, stripe_source):
        stripe_token = StripeToken(stripe_source, self.id)
        db.session.add(stripe_token)
        db.session.commit()
        return stripe_token.id

    def get_source(self):
        stripe_object = db.Query(StripeToken).filter_by(customer_id=self.id).first()

        return stripe_object.source



class StripeToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)
    customer_id = db.Column(db.Integer)


    def __init__(self, source, cust_id):
        self.source = source
        self.customer_id = cust_id

    def __repr__(self):
        return '<Token %r>' % self.source


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_transaction = db.Column(db.Integer)
    amount = db.Column(db.Float)
    name = db.Column(db.String)
    description = db.Column(db.String)
    recurring = db.Column(db.Boolean)
    sale_type = (db.Column(db.String(50)))
    customer_id = db.Column(db.Integer)

    def __init__(self, name, descript, stripe_transaction, amount, recurring, sale_type, customer_id):
        self.name = name
        self.description = descript
        self.stripe_transaction = stripe_transaction
        self.amount = amount
        self.recurring = recurring
        self.sale_type = sale_type
        self.customer_id = customer_id

    def __repr__(self):
        return '<User %r>' % self.sale_type + " " + self.name + " - " + self.amount


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64))
    # is_admin = db.Column(db.Boolean())
    sessionhash = db.Column(db.String(64), unique=True)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = md5(password).hexdigest()
        self.sessionhash = md5(username + self.password + email).hexdigest()
        # self.is_admin = is_admin

    def __repr__(self):
        return '<User %r>' % self.username

    def login(self, password, ip, user_agent):
        phash = md5(password).hexdigest()
        authenticated = self.password == phash
        la = LoginAttempts(self, authenticated, ip, user_agent)
        db.session.add(la)
        db.session.commit()
        if self.password == phash:
            return self.sessionhash
        return "logout"


class LoginAttempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    success = db.Column(db.Boolean())
    time_at = db.Column(db.DateTime())
    ip = db.Column(db.String(256))
    user_agent = db.Column(db.String(256))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('login_attempts', lazy='dynamic'))

    def __init__(self, user, success, ip, user_agent):
        self.success = success
        self.user = user
        self.ip = ip
        self.user_agent = user_agent
        self.time_at = datetime.utcnow()

