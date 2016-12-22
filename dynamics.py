from flask import request,session,jsonify

from t import builtin_dynamics
import db
import forms
import stripe_handlers


def create_account():
    if request.method != "POST":
        return {}
    new_user = db.User(request.form.get("username"), request.form.get("email"), request.form.get("password"))
    db.db.session.add(new_user)
    db.db.session.commit()
    return {"message": "User created successfully.",
            "username": request.form.get("username")}


def add_lead():
    email_address = request.form['email']
    lname = request.form['last_name']
    fname = request.form['first_name']

    billing_address = request.form['billing_address']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    zip_code = request.form['zip_code']
    customer = db.Customer(first_name=fname, last_name=lname, billing_address=billing_address, city=city, state=state,
                           country=country, zip_code=zip_code)
    db.db.session.add(customer)
    db.db.session.commit()
    return customer.id


def create_lead():
    lead_form = forms.BaseApiLeadForm(request.form)
    if lead_form.validate():
        lead_id = add_lead()
        session['customer_id'] = int(lead_id)

        message = {'result': "succcess"}

    else:
        message = {'result': 'failurd'}
    return jsonify(message)


def charge_customer():
    customer = db.Customer.query.filter_by(id=session['customer_id']).first()

    if customer:
        if request.form['tos'] == 'main_sale':
            orderform = forms.InitialOrderForm(request.form)
            if orderform.validate():
                stripe_customer_id = stripe_handlers.create_stripe_customer(customer.id, customer.email,
                                                                            request.form['stripeToken'])
                if stripe_customer_id:
                    customer.stripe_customer_id = stripe_customer_id
                    db.db.session.add(customer)
                    db.db.session.commit()

    orderform = forms.OrderForm(request.form)
    if orderform.validate():
        if request.form['recurring']:
            subscription_id = stripe_handlers.subscribe_customer(request.form['name'], request.form['amount'],
                                                                 customer.stripe_customer_id)
            result = True
            message_stripe_transaction = "Subscription placeholder"
        else:
            result, message_stripe_transaction = stripe_handlers.stripe_charge(customer.stripe_customer_id,
                                                                               request.form['amount'],
                                                                               request.form['description'])
        if result:  # message = charge.receipt_number, if true
            customer.create_order(stripe_transaction=message_stripe_transaction, amount=request.form['amount'],
                                  recurring=request.form['recurring'], sales_type=request.form['tos'],
                                  purchaser=customer)
            return jsonify({"result": 'success'})
        else:
            return jsonify({'result': message_stripe_transaction})

    else:
        return jsonify({'result': 'failed', 'errors': orderform.errors})

def index(user=None):
    return {}


def api_test():
    return {"this_is": "SPARTAAAAA"}


pub_sources = {	"index": index, "create_account": builtin_dynamics.create_account}
priv_sources = {	"index": index}

api_sources = {		"leads/" :create_lead ,"purchase/" :charge_customer}
