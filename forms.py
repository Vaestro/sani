from flask.ext.wtf import Form
from wtforms import TextField, StringField, PasswordField, BooleanField, SubmitField, \
FloatField, IntegerField, validators, TextAreaField, RadioField, SelectField, HiddenField
from wtforms.validators import Required
from wtforms.fields.html5 import EmailField

from models import db, User

class UserForm(Form):
	name = StringField("Name")
	email = EmailField("Email", [validators.Required(), validators.Email()])
	gender = RadioField("Gender", choices=[("Male","Male"),("Female","Female")], default="Male")
	act = SelectField("Which of these describes your daily activity?",
		     choices=[("Sedentary","Sedentary"),
		     ("Low","Lightly Active"),
		     ("Active","Moderately Active"),
		     ("Very Active","Very Active")])
	weight = FloatField("Weight",  [validators.Required("Please enter your weight(lb)."), validators.NumberRange(min=50,max=500,message="Please enter a valid weight")])
	#height = FloatField("Height(cm)",  [validators.Required("Please enter your height(cm).")])
	weightUnit = SelectField("Unit", choices=[("lb", "lb"), ("kg", "kg")], default="lb")

	height = SelectField("Height", coerce=float, choices=[(152.4, "5\'0 - 152.4cm"), (154.9, "5\'1 - 154.9cm"),
		(157.4, "5\'2 - 157.4cm"),(160, "5\'3 - 160cm"),(162.5, "5\'4 - 162.5cm"),
		(165.1, "5\'5 - 165.1cm"),(167.6, "5\'6 - 167.6cm"),(170.1, "5\'7 - 170.1cm"),
		(172.7, "5\'8 - 172.7cm"),(175.2, "5\'9 - 175.2cm"),(177.8, "5\'10 - 177.8cm"),
		(180.3, "5\'11 - 180.3cm"),
		(182.8, "6\'0 - 182.8cm"),(185.4, "6\'1 - 185.4cm"),(187.9, "6\'2 - 187.9cm"),
		(190.5, "6\'3 - 190.5cm"),(193.0, "6\'4 - 193.0cm"),(195.8, "6\'5 - 195.8cm"),(198.1, "6\'6 - 198.1cm"),(200.7, "6\'7 - 200.7cm")])

	goal = RadioField("Do you have a weight goal?", \
		     choices=[("Gain","Gain Weight"),("Maintain","Maintain Weight"),\
		     ("Lose","Lose Weight")], default="Maintain")

	age = IntegerField("Age",  [validators.Required("Please enter your age.")])

	submit = SubmitField('Submit')

class IngredientsForm(Form):
	ingredientJson = TextAreaField("ingredientJson")
	#hidden = HiddenField("json",  [validators.Length(min=4, max=200)] )
	deviation = TextAreaField("deviation")
	nutrient = TextAreaField("nutrient")
	nutrient2 = TextAreaField("nutrient2")
	quantity = SelectField("Quantity", choices=[(7, "$35.00 - 7 Meals ($5/meal)"), (14, "$59.00 - 14 Meals ($4.25/meal)"), (21, "$84.00 - 21 Meals ($4/meal)")])
	subscribe = BooleanField("Subscribe and save")
	submit = SubmitField('Continue')
