from flask import redirect, render_template, request, send_from_directory, jsonify, session

import db
from db import app
import dynamics
import forms
import stripe_handlers


class SimpleMultiDict(dict):
    def getlist(self, key):
        return self[key] if type(self[key]) == list else [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'


def create_dict(dictt):
    new_dict = SimpleMultiDict()
    for key in dictt:
        new_dict[key] = dictt.get(key, "")
    return new_dict


def add_lead(dicttt):
    new_dict = create_dict(dicttt)
    email_address = dicttt['email']
    lname = dicttt['lastName']
    fname = dicttt['firstName']

    billing_address = dicttt['address']
    city = dicttt['city']
    state = dicttt['state']
    country = dicttt['country']
    zip_code = dicttt['zip']
    email = dicttt['email']
    customer = db.Customer(email=email, first_name=fname, last_name=lname, billing_address=billing_address, city=city,
                           state=state,
                           country=country, zip_code=zip_code)
    db.db.session.add(customer)
    db.db.session.commit()
    return customer.id


@app.route('/')
def reroot():
    return redirect('/pub/')


@app.route('/leads', methods=["GET", "POST"])
def create_lead():
    new_dict = create_dict(request.form)

    lead_form = forms.BaseApiLeadForm(new_dict)
    if lead_form.validate():
        lead_id = add_lead(new_dict)
        session['customer_id'] = lead_id
        dataz = {"DATA": session['customer_id']}
        return jsonify(dataz)

        # message = {'result': "succcess"}

    else:
        message = {'result': 'failurd'}
    return jsonify(message)


@app.route('/purchase', methods=["GET", "POST"])
def charge_customer():
    cid = session.get('customer_id', 'No Sesssion')
    print cid
    db.logger.info("cid is " + str(cid))
    customer = db.Customer.query.filter_by(id=int(cid)).first()
    new_dict = create_dict(request.form)
    if customer:
        if new_dict['tos'] == 'main_sale':
            orderform = forms.InitialOrderForm(new_dict)
            if orderform.validate():
                customer_result, stripe_source = stripe_handlers.create_stripe_customer(customer.email,
                                                                                        new_dict['stripeToken'])
                if customer_result:
                    customer.add_stripe_source(stripe_source)
                    db.db.session.add(customer)
                    db.db.session.commit()
                else:
                    return jsonify({'status': customer_result, 'message': stripe_source})

        orderform = forms.OrderForm(new_dict)
        if orderform.validate():
            stripe_source = customer.get_source()
            if new_dict['recurring']:
                subscription_id = stripe_handlers.subscribe_customer(new_dict['name'], new_dict['amount'],
                                                                     stripe_source)
                result = True
                message_stripe_transaction = "Subscription placeholder"
            else:
                result, message_stripe_transaction = stripe_handlers.stripe_charge(stripe_source, new_dict['amount'],
                                                                                   new_dict['description'])

            if result:  # message = charge.receipt_number, if true
                customer.create_order(stripe_transaction=message_stripe_transaction, name=new_dict['name'],
                                      amount=new_dict['amount'],
                                      description=new_dict['description'],
                                      recurring=new_dict['recurring'], sales_type=new_dict['tos'])
                return jsonify({"result": 'success'})
            else:
                return jsonify({'result': "session doesnt exist"})

        else:
            return jsonify({'result': 'failed', 'errors': orderform.errors})

if __name__ == '__main__':
    app.run()