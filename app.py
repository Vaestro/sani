import os
import math
import uuid
from flask import Flask, render_template, flash, redirect, session, url_for, request, g, send_from_directory, make_response, jsonify, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy, get_debug_queries
from flask.ext.bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from flask_sslify import SSLify
from forms import UserForm, IngredientsForm
from models import User, SaniOrder, db
import json
import requests
import stripe

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
sslify = SSLify(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sanilife:sanilife@sanidb.c2pz7qitscgg.us-west-2.rds.amazonaws.com:3306/sanidb'

# Uncomment the line below if you want to work with a local DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

######################################################################

db.init_app(app)
with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

bootstrap = Bootstrap(app)

@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    ingredientform = IngredientsForm()

    if request.method == 'POST':
        return render_template('index.html', ingredientform=ingredientform)
    elif request.method == 'GET':
        return render_template('index.html', ingredientform=ingredientform)


@app.route('/', methods=['GET', 'POST'])
@app.route('/user', methods=['GET', 'POST'])
def user():
    form = UserForm()

    if request.method == 'POST':

        if form.email.data:
            email = form.email.data
            session['name'] = form.name.data
            session['gender'] = form.gender.data
            session['act'] = form.act.data
            session['weight'] = form.weight.data
            session['height'] = form.height.data
            session['goal'] = form.goal.data
            session['age'] = form.age.data

        elif session['email']:
            email = session['email']

        session['email'] = email

        registered_user = User.query.filter_by(email=email).first()
        if registered_user:
            return render_template('error.html')
        else:
            if form.weightUnit.data == "kg":
                session['weight'] = session['weight'] * 2.20462262

            A = session['weight'] / 2.2 * 9.99
            B = float(session['height']) * 6.25
            C = session['age'] * 4.92
            if session['gender'] == "Male":
                D = 5
            else:
                D = -161
            BMR = math.floor(A + B - C + D)
            if session['act'] == "Sedentary":
                F = 1.2
            elif session['act'] == "Low":
                F = 1.4
            elif session['act'] == "Active":
                F = 1.6
            else:
                F = 1.8
            if session['goal'] == "Gain":
                G = 1.2
            elif session['goal'] == "Maintain":
                G = 1.0
            else:
                G = 0.8

            # Calorie Target
            TDEE = G * F * BMR
            if TDEE < 1758:
                TDEE = 1758

            protein = session['weight'] * 0.88
            # Calculate the fat
            fat = TDEE * 0.25 / 9
            if fat < 60.07:
                fat = 60.07
            # Calculate the carbs
            carbs = (TDEE - protein * 4 - fat * 9) / 4
            if carbs < 225.9:
                carbs = 225.9
            # Recalculate the protein
            protein = (TDEE - carbs * 4 - fat * 9) / 4
            # session['calories'] = TDEE
            # session['protein'] = protein
            # session['fat'] = fat
            # session['carbs'] = carbs
            if form.email.data:
                session['calories'] = TDEE
                session['protein'] = protein
                session['fat'] = fat
                session['carbs'] = carbs

            ingredientform = IngredientsForm()
            # hiddenform = ingredientform.hidden.data
            ingredientJson = ingredientform.ingredientJson.data

            ingredientJsonLoads = None
            nutrientMerge = None
            ratio = {}
            ratio2 = {}
            ratioJson1 = {}
            ratioJson2 = {}
            pieChartData = {}

            if ingredientJson:

                ingredientJsonDeleteComma = ingredientJson[0:-2] + '}'
                ingredientJsonLoads = json.loads(ingredientJsonDeleteComma)
                brown = int(ingredientJsonLoads['Brown Rice Flour Brown'])
                protein_blend = int(ingredientJsonLoads['Protein Blend'])
                carb_blend = int(ingredientJsonLoads['Carb Blend'])
                fat_blend = int(ingredientJsonLoads['Fat Blend'])

                nutrientDeleteComma = ingredientform.nutrient.data[0:-2] + '}'
                nutrient2DeleteComma = ingredientform.nutrient2.data[
                    0:-2] + '}'
                # nutrientMerge = json.loads(nutrientDeleteComma) + json.loads(nutrient2DeleteComma)

                nutrientMerge = json.loads(nutrientDeleteComma).copy()
                nutrientMerge.update(json.loads(nutrient2DeleteComma))

                # ratio = {
                #		 'carbs':nutrientMerge['carb']/nutrientMerge['calories'],
                #		 'protein':nutrientMerge['protein']/nutrientMerge['calories'],
                #		 'fat': nutrientMerge['protein']/nutrientMerge['calories']}
                ratio['calories-Amount'] = nutrientMerge['calories']
                ratio['carbs'] = nutrientMerge['carbs'] * 4 * \
                    1000 // nutrientMerge['calories'] / 10.0
                ratio['protein'] = nutrientMerge['protein'] * \
                    4 * 1000 // nutrientMerge['calories'] / 10.0
                ratio['fat'] = nutrientMerge['fat'] * 9 * \
                    1000 // nutrientMerge['calories'] / 10.0
                ratio['carbs-Amount'] = nutrientMerge['carbs']
                ratio['protein-Amount'] = nutrientMerge['protein']
                ratio['fat-Amount'] = nutrientMerge['fat']
                ratio['fiber-Amount'] = nutrientMerge['fiber']
                ratio['saturated-fat-Amount'] = nutrientMerge['saturated-fat']

                # del
                # del nutrientMerge['Omega-6:Omega-3']

                tempNutrition = {
                    "soluble-fiber_max": 0,
                    "soluble-fiber": 0,
                    "saturated-fat_max": 999,
                    "saturated-fat": 20,
                    "polyunsaturated-fat_max": 999,
                    "polyunsaturated-fat": 1,
                    "monounsaturated-fat_max": 999,
                    "monounsaturated-fat": 1,
                    "insoluble-fiber_max": 0,
                    "insoluble-fiber": 0,
                    "name": "Sebastian",
                    "calories": 2833,
                    "calories_max": 0,
                    "carbs": 404,
                    "carbs_max": 0,
                    "protein": 142,
                    "protein_max": 0,
                    "fat": 63,
                    "fat_max": 0,
                    "omega_3": 1.6,
                    "omega_3_max": 0,
                    "omega_6": 17,
                    "omega_6_max": 0,
                    "fiber": 28,
                    "fiber_max": 0,
                    "cholesterol": 0,
                    "cholesterol_max": 0,
                    "calcium": 1,
                    "calcium_max": 2.5,
                    "chloride": 2.3,
                    "chloride_max": 3.6,
                    "chromium": 35,
                    "chromium_max": 0,
                    "copper": 0.9,
                    "copper_max": 10,
                    "iodine": 150,
                    "iodine_max": 1100,
                    "iron": 8,
                    "iron_max": 45,
                    "magnesium": 420,
                    "magnesium_max": 770,
                    "manganese": 2.3,
                    "manganese_max": 11,
                    "molybdenum": 45,
                    "molybdenum_max": 2000,
                    "phosphorus": 0.7,
                    "phosphorus_max": 4,
                    "potassium": 3.5,
                    "potassium_max": 0,
                    "selenium": 55,
                    "selenium_max": 400,
                    "sodium": 1.5,
                    "sodium_max": 2.3,
                    "sulfur": 2,
                    "sulfur_max": 0,
                    "zinc": 11,
                    "zinc_max": 40,
                    "vitamin_a": 3000,
                    "vitamin_a_max": 10000,
                    "vitamin_b6": 1.3,
                    "vitamin_b6_max": 100,
                    "vitamin_b12": 2.4,
                    "vitamin_b12_max": 0,
                    "vitamin_c": 90,
                    "vitamin_c_max": 2000,
                    "vitamin_d": 200,
                    "vitamin_d_max": 4000,
                    "vitamin_e": 15,
                    "vitamin_e_max": 1000,
                    "vitamin_k": 120,
                    "vitamin_k_max": 0,
                    "thiamin": 1.2,
                    "thiamin_max": 0,
                    "riboflavin": 1.3,
                    "riboflavin_max": 0,
                    "niacin": 16,
                    "niacin_max": 35,
                    "folate": 400,
                    "folate_max": 1000,
                    "pantothenic": 5,
                    "pantothenic_max": 0,
                    "biotin": 30,
                    "biotin_max": 0,
                    "choline": 550,
                    "choline_max": 3500
                }

                if session['gender'] == "Male" and session['age'] > 50:
                    tempNutrition["calcium"] = 1.2
                    tempNutrition["chloride"] = 2.0
                    tempNutrition["chromium"] = 30
                    tempNutrition["sodium"] = 1.3
                    tempNutrition["vitamin_b6"] = 1.7
                    tempNutrition["vitamin_d"] = 400

                if session['gender'] == "Female" and session['age'] <= 50:
                    tempNutrition = {
                        "soluble-fiber_max": 0,
                        "soluble-fiber": 0,
                        "saturated-fat_max": 999,
                        "saturated-fat": 20,
                        "polyunsaturated-fat_max": 999,
                        "polyunsaturated-fat": 1,
                        "monounsaturated-fat_max": 999,
                        "monounsaturated-fat": 1,
                        "insoluble-fiber_max": 0,
                        "insoluble-fiber": 0,
                        "name": "Sebastian",
                        "calories": 2833,
                        "calories_max": 0,
                        "carbs": 404,
                        "carbs_max": 0,
                        "protein": 142,
                        "protein_max": 0,
                        "fat": 63,
                        "fat_max": 0,
                        "omega_3": 1.6,
                        "omega_3_max": 0,
                        "omega_6": 17,
                        "omega_6_max": 0,
                        "fiber": 28,
                        "fiber_max": 0,
                        "cholesterol": 0,
                        "cholesterol_max": 0,
                        "calcium": 1,
                        "calcium_max": 2.5,
                        "chloride": 2.3,
                        "chloride_max": 3.6,
                        "chromium": 25,
                        "chromium_max": 0,
                        "copper": 0.9,
                        "copper_max": 10,
                        "iodine": 150,
                        "iodine_max": 1100,
                        "iron": 18,
                        "iron_max": 45,
                        "magnesium": 320,
                        "magnesium_max": 770,
                        "manganese": 1.8,
                        "manganese_max": 11,
                        "molybdenum": 45,
                        "molybdenum_max": 2000,
                        "phosphorus": 0.7,
                        "phosphorus_max": 4,
                        "potassium": 3.5,
                        "potassium_max": 0,
                        "selenium": 55,
                        "selenium_max": 400,
                        "sodium": 1.5,
                        "sodium_max": 2.3,
                        "sulfur": 2,
                        "sulfur_max": 0,
                        "zinc": 8,
                        "zinc_max": 40,
                        "vitamin_a": 2333,
                        "vitamin_a_max": 10000,
                        "vitamin_b6": 1.3,
                        "vitamin_b6_max": 100,
                        "vitamin_b12": 2.4,
                        "vitamin_b12_max": 0,
                        "vitamin_c": 75,
                        "vitamin_c_max": 2000,
                        "vitamin_d": 200,
                        "vitamin_d_max": 4000,
                        "vitamin_e": 15,
                        "vitamin_e_max": 1000,
                        "vitamin_k": 90,
                        "vitamin_k_max": 0,
                        "thiamin": 1.1,
                        "thiamin_max": 0,
                        "riboflavin": 1.1,
                        "riboflavin_max": 0,
                        "niacin": 14,
                        "niacin_max": 35,
                        "folate": 400,
                        "folate_max": 1000,
                        "pantothenic": 5,
                        "pantothenic_max": 0,
                        "biotin": 30,
                        "biotin_max": 0,
                        "choline": 425,
                        "choline_max": 3500
                    }

                if session['gender'] == "Female" and session['age'] > 50:
                    tempNutrition = {
                        "soluble-fiber_max": 0,
                        "soluble-fiber": 0,
                        "saturated-fat_max": 999,
                        "saturated-fat": 20,
                        "polyunsaturated-fat_max": 999,
                        "polyunsaturated-fat": 1,
                        "monounsaturated-fat_max": 999,
                        "monounsaturated-fat": 1,
                        "insoluble-fiber_max": 0,
                        "insoluble-fiber": 0,
                        "name": "Sebastian",
                        "calories": 2833,
                        "calories_max": 0,
                        "carbs": 404,
                        "carbs_max": 0,
                        "protein": 142,
                        "protein_max": 0,
                        "fat": 63,
                        "fat_max": 0,
                        "omega_3": 1.6,
                        "omega_3_max": 0,
                        "omega_6": 17,
                        "omega_6_max": 0,
                        "fiber": 28,
                        "fiber_max": 0,
                        "cholesterol": 0,
                        "cholesterol_max": 0,
                        "calcium": 1,
                        "calcium_max": 2.5,
                        "chloride": 2.0,
                        "chloride_max": 3.6,
                        "chromium": 20,
                        "chromium_max": 0,
                        "copper": 0.9,
                        "copper_max": 10,
                        "iodine": 150,
                        "iodine_max": 1100,
                        "iron": 8,
                        "iron_max": 45,
                        "magnesium": 320,
                        "magnesium_max": 770,
                        "manganese": 1.8,
                        "manganese_max": 11,
                        "molybdenum": 45,
                        "molybdenum_max": 2000,
                        "phosphorus": 0.7,
                        "phosphorus_max": 3,
                        "potassium": 3.5,
                        "potassium_max": 0,
                        "selenium": 55,
                        "selenium_max": 400,
                        "sodium": 1.3,
                        "sodium_max": 2.3,
                        "sulfur": 2,
                        "sulfur_max": 0,
                        "zinc": 8,
                        "zinc_max": 40,
                        "vitamin_a": 2333,
                        "vitamin_a_max": 10000,
                        "vitamin_b6": 1.5,
                        "vitamin_b6_max": 100,
                        "vitamin_b12": 2.4,
                        "vitamin_b12_max": 0,
                        "vitamin_c": 75,
                        "vitamin_c_max": 2000,
                        "vitamin_d": 400,
                        "vitamin_d_max": 4000,
                        "vitamin_e": 15,
                        "vitamin_e_max": 1000,
                        "vitamin_k": 90,
                        "vitamin_k_max": 0,
                        "thiamin": 1.1,
                        "thiamin_max": 0,
                        "riboflavin": 1.1,
                        "riboflavin_max": 0,
                        "niacin": 14,
                        "niacin_max": 35,
                        "folate": 400,
                        "folate_max": 1000,
                        "pantothenic": 5,
                        "pantothenic_max": 0,
                        "biotin": 30,
                        "biotin_max": 0,
                        "choline": 425,
                        "choline_max": 3500
                    }

                for item in nutrientMerge:

                    ratio2[item] = int(nutrientMerge[item] *
                                       100 // tempNutrition[item])

                ratio['fiber'] = int(nutrientMerge['fiber'] *
                                     100 // tempNutrition['fiber'])
                ratio['saturated-fat'] = ratio2['saturated-fat']
    ######################## First Json FIle ##################################
                ratioJson1 = ratio2.copy()
                ratioJson1.update(ratio)
                ratioJson1['sodium-Amount'] = nutrientMerge['sodium']
                ratioJson1['potassium-Amount'] = nutrientMerge['potassium']

                del ratioJson1['polyunsaturated-fat']
                del ratioJson1['monounsaturated-fat']
    ######################## Second Json File ############################
                ratioJson2 = nutrientMerge.copy()
                ratioJson2.update(ratio)
    ######################## Database #####################################

                # pieChartData = {'carbs': ratio['carbs'], 'protein': ratio['protein'], 'fat': ratio['fat']}
                # pieChartData['carbs'] = ratio['carbs']
                # pieChartData['protein'] = ratio['protein']
                # pieChartData['fat'] = ratio['fat']
                pieChartData = {'carbs': nutrientMerge[
                    'carbs'] * 4, 'protein': nutrientMerge['protein'] * 4, 'fat': nutrientMerge['fat'] * 9}

                newUser = User(name=session['name'],
                               email=session['email'],
                               gender=session['gender'],
                               act=session['act'],
                               weight=session['weight'],
                               height=session['height'],
                               goal=session['goal'],
                               age=session['age'],
                               calories=session['calories'],
                               protein=session['protein'],
                               fat=session['fat'],
                               carbs=session['carbs'],
                               ingredientJson=ingredientJsonDeleteComma,
                               brown=brown,
                               protein_blend=protein_blend,
                               carb_blend=carb_blend,
                               fat_blend=fat_blend,
                               deviation=ingredientform.deviation.data,
                               nutrient=nutrientDeleteComma,
                               nutrient2=nutrient2DeleteComma,
                               nutrientMerge=str(nutrientMerge),
                               ratioJson1=str(ratioJson1),
                               ratioJson2=str(ratioJson2),
                               )

                db.session.add(newUser)
                db.session.commit()

            return render_template('index.html', calories=TDEE,  protein=protein,
                                   fat=fat, carbs=carbs, gender=session['gender'], age=session['age'],
                                   email=email, ingredientform=ingredientform,
                                   ingredientJsonLoads=ingredientJsonLoads, nutrientMerge=nutrientMerge,
                                   ratio=ratio, ratio2=ratio2, ratioJson1=str(ratioJson1),
                                   ratioJson2=str(ratioJson2), key=stripe_keys['publishable_key'])

    else:
        return render_template('user.html', form=form)


@app.route('/buy', methods=['POST'])
def buy():
    quantity = request.form['quantity']
    amount = request.form['amount']
    email = request.form['email']
    token = request.form['stripeToken']

    customer = stripe.Customer.create(
        email=email,
        source=token
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Sani Checkout'
    )

    order = SaniOrder(
        uuid=str(uuid.uuid4()),
        email=email,
        quantity=quantity,
        amount=amount
    )

    db.session.add(order)
    db.session.commit()

    return render_template('buy.html', amount=amount)

# Test the connection of MySQL
@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
