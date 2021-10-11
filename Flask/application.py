from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename
from flask import send_file

import pandas as pd
import numpy as np
import pickle

import random
import string
import os

# ML Packages
from sklearn.feature_extraction.text import CountVectorizer

# Loading our ML Model
rf_use_hours = pickle.load(open("./models/RandomForest_use_hours.pkl", "rb"))
rf_use_salaries = pickle.load(open("./models/RandomForest_use_salaries.pkl", "rb"))
rf_is_productive = pickle.load(open("./models/RandomForest_is_productive.pkl", "rb"))

# Loading the String Classifier
string_classifier = pickle.load(open("./models/string_classifier.pkl", "rb"))


application = app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Read from user input
    # Note: The input must be in the order: Total Dollars, Total Hours, Hourly Rate
    input_features = [x for x in request.form.values()]
    payment_type_string = str.upper(str(input_features[0]))
    float_features = input_features[1:]
    float_features = np.array([float(x) for x in float_features])
    float_features = float_features.reshape((1, -1))

    # Prediction
    if payment_type_string in string_classifier:
        pred_use_hours = string_classifier[payment_type_string]['use_hours']
        pred_use_salaries = string_classifier[payment_type_string]['use_salaries']
        pred_is_productive = string_classifier[payment_type_string]['is_productive']

    else:
        pred_use_hours = rf_use_hours.predict(float_features)[0]
        pred_use_salaries = rf_use_salaries.predict(float_features)[0]
        pred_is_productive = rf_is_productive.predict(float_features)[0]


    return render_template('results.html', payment_type_string = payment_type_string, pred_use_hours = pred_use_hours, pred_use_salaries = pred_use_salaries, pred_is_productive = pred_is_productive,
    total_dollars = float_features[0][0], total_hours = float_features[0][1], hourly_rate = float_features[0][2])


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        # Read File to DataFrame
        data = pd.read_excel(f.filename)

        # Check if columns match requirement
        if not list(data.columns) == ['pay_type_description', 'total_dollars', 'total_hours', 'hourly_rate']:
            return "ERROR! Names in uploaded file do not match requirements!"

        # Initialize Results
        use_hours = []
        use_salaries = []
        is_productive = []

        # Prediction
        for index, row in data.iterrows():
            pay_type_description = str(row.pay_type_description).upper()

            if pay_type_description in string_classifier:
                info = string_classifier[pay_type_description]
                use_hours.append(info["use_hours"])
                use_salaries.append(info["use_salaries"])
                is_productive.append(info["is_productive"])

            else:
                total_dollars = row.total_dollars
                total_hours = row.total_hours
                hourly_rate = row.hourly_rate

                features = np.array([total_dollars, total_hours, hourly_rate])
                features = features.reshape((1, -1))

                # print(features)
                # print("---------")

                vals = features[0]
                for i in range(3):
                    if type(vals[i]) != np.float64:
                        try: 
                            temp = vals[i]
                            vals[i] = np.float(temp)
                            # print("Converted from " + str(temp) + "to " + str(vals[i]))
                        except:
                            # If value is not float and cannot be converted to float (possibly because the value is missing or other illegal symbols involed):
                            vals[i] = 0
                            # print(str(vals[i]) + " cannot  be converted; being set to 0")


                use_hours.append(round(rf_use_hours.predict(features)[0]))
                use_salaries.append(round(rf_use_salaries.predict(features)[0]))
                is_productive.append(round(rf_is_productive.predict(features)[0]))

        data["use_hours"] = use_hours
        data["use_salaries"] = use_salaries
        data["is_productive"] = is_productive

        # filename = "./result" + randomString(6) + ".xlsx"
        # TODO: FIGURE OUT A WAY TO DELETE FILE AFTER RETURN TO AVOID MEMORY LEAK

        os.remove(f.filename)

        filename = "./result.xlsx"
        data.to_excel(filename)

        return send_file(filename) 


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ == '__main__':
	app.run(debug=True)