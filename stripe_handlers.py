__author__ = 'hamik112'
import stripe

import db

stripe.api_key = " sk_test_bwV4sv6v8j6czoo8O4M3YkM4"
def create_stripe_customer(email, stripe_token):
    try:
        stripe_customer = stripe.Customer.create(email=email, source=stripe_token)
        if stripe_customer.id:
            return True, stripe_customer.id
    except stripe.error.CardError as e:
        body = e.json_body
        err  = body['error']
        return False, err
def subscribe_customer(verbose_name, amount, customer_id, interval="month", currency="usd"):
    unique_id = verbose_name.replace(" ", "_")
    unique_id = unique_id.replace("'", "")
    unique_id = unique_id.lower()
    current_plans = stripe.Plan.list()
    subscribe_id = ''
    for plan in current_plans.data:
        if plan.id == unique_id:
            subscribe_id = plan.id
    stripe.Plan.create(name=verbose_name, id=unique_id, interval=interval, currency=currency, amount=amount)
    subscribe_id = unique_id
    subscriber = stripe.Subscription.create(customer=customer_id.id, plan=subscribe_id)
        return subscriber.status,subscriber.id

def stripe_charge(cid, charge_amount, charge_descripton):
    insufficient_message = 'Your transaction was declined due to insufficient. Please try a different card.'
    issuer_not_available = 'Please wait a few minutes and try this order again. If you still have trouble with your transaction'
    generic_decline = 'Please try a different card or call your bank to find out why out why this transaction was declined.'

    user = db.Customer.query.filter_by(id=cid).first()
    if user:
        stripe_source = user.get_source()
        try:
            charge = stripe.Charge.create(
                customer=stripe_source,
                amount=charge_amount,
                currency='usd',
                description=charge_descripton)
            if charge.outcome.network_status == "approved_by_network":
                return True, charge.receipt_number
            elif charge.outcome.network_status == 'issuer_not_available':
                return False, issuer_not_available
            elif charge.outcome.network_status == "insufficient_funds":
                return False, insufficient_message
            else:
                return False,
        except stripe.CardError as e:
            return False, e
    else:
        e = "User Does Not Have Payment Method on File"
        return False, e
