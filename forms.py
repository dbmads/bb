from wtforms import Form, StringField, TextAreaField, validators, IntegerField, FieldList, FormField, BooleanField, \
    FloatField, SelectField


class Form_Record_Add(Form):
    title = StringField('title', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    description = TextAreaField('description',
                                validators=[validators.Length(max=200, message='max 200 characters')])


class OrderForm(Form):
    name = StringField('product_name', validators=[validators.DataRequired("product_name is required")])
    description = StringField('description', validators=[validators.DataRequired("description is required")])

    amount = FloatField('charge_amount', validators=[validators.DataRequired("amount is required")])
    recurring = BooleanField('recurring', validators=[validators.DataRequired("recurring required")])
    tos = SelectField('transaction_type', validators=[validators.DataRequired()],
                      choices=[("main_sale", "main_sale"), ("upsell1", "upsell1"), ("upsell2", "upsell2")])


class InitialOrderForm(OrderForm):
    stripeToken = StringField('stripeToken', validators=[validators.DataRequired()])


class BaseApiLeadForm(Form):
    email = StringField('email',
                        validators=[validators.DataRequired("Email is required"), validators.Length(min=3, max=25),
                                    validators.Email()])
    firstName = StringField('firstName', validators=[validators.DataRequired("First name is required"),
                                                     validators.Length(min=2, max=30)])

    lastName = StringField('lastName', validators=[validators.DataRequired("Last name is required"),
                                                   validators.Length(min=2, max=30)])

    address = StringField('address', validators=[validators.DataRequired("Address is required"),
                                                 validators.Length(min=10, max=255)])
    city = StringField('city',
                       validators=[validators.DataRequired("City is required"), validators.Length(min=1, max=55)])
    phone = StringField('phone', validators=[validators.DataRequired("Zip code is required")])
    zip = IntegerField('zip',
                       validators=[validators.DataRequired("Zip code is required"),
                                   validators.NumberRange(00000, 99999)])
    state = StringField('state',
                        validators=[validators.DataRequired("State is required"), validators.Length(min=2, max=2)])
    country = StringField('country', validators=[validators.DataRequired("Country is required")])


class OnePagePurchaseForm(Form):
    email = StringField('email',
                        validators=[validators.DataRequired("Email is required"), validators.Length(min=3, max=25),
                                    validators.Email()])
    firstName = StringField('fname', validators=[validators.DataRequired("First name is required"),
                                                 validators.Length(min=2, max=30)])

    lastName = StringField('lname', validators=[validators.DataRequired("Last name is required"),
                                                validators.Length(min=2, max=30)])

    address = StringField('address', validators=[validators.DataRequired("Address is required"),
                                                 validators.Length(min=10, max=255)])
    city = StringField('city',
                       validators=[validators.DataRequired("City is required"), validators.Length(min=1, max=55)])
    phone = IntegerField('phone_number', validators=[validators.DataRequired("Zip code is required")])
    zip = IntegerField('zip_code',
                       validators=[validators.DataRequired("Zip code is required"), validators.Length(min=5, max=5)])
    state = StringField('state',
                        validators=[validators.DataRequired("State is required"), validators.Length(min=2, max=2)])
    country = StringField('country', validators=[validators.DataRequired("Country is required")])
    name = StringField('product_name', validators=[validators.DataRequired("product_name is required")])
    description = StringField('description', validators=[validators.DataRequired("description is required")])

    amount = FloatField('charge_amount', validators=[validators.DataRequired("amount is required")])
    recurring = BooleanField('recurring', validators=[validators.DataRequired("recurring required")],
                             choices=[True, False])
    tos = BooleanField('transaction_type', validators=[validators.DataRequired()],
                       choices=["main_sale", "upsell1", "upsell2"])

    stripeToken = StringField('stripeToken', validators=[validators.DataRequired()])
