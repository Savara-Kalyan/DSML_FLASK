from flask import Flask , request
import pickle
# initialization of app
app = Flask(__name__)


model_pickle = open('./artifacts/classifier.pkl' , 'rb')

clf = pickle.load(model_pickle)

@app.route('/ping' , methods = ['GET'])
def ping():
    return {"Message" : "Hi there , this endpoint is working"}

@app.route("/template" , methods = ['GET'])
def get_template():
    return{
        "gender" : "Male/Female",
        "married" : "Married/Unmarried",
        "applicant_income" : "<Numeric Salary>" ,
        "loan_amount" : "<Numeric loan amount>",
        "credit_history" : "Cleared Debts/Uncleared Debts"}

@app.route('/predict' , methods = ['POST' , 'GET'])
def predict():
    """
        Returns loan application status
    """

    loan_req = request.get_json()


    if loan_req['gender'] == 'Male':
        gender = 0
    else:
        gender = 1

    if loan_req['married'] == 'Unmarried':
        marital_status = 0
    else:
        marital_status = 1

    if loan_req['credit_history'] == 'Uncleared Debts':
        credit_status = 0
    else:
        credit_status = 1

    applicant_income = loan_req['applicant_income']

    loan_amount = loan_req['loan_amount']

    result = clf.predict([[gender , marital_status , applicant_income , loan_amount , credit_status]])


    if result == 0:
        pred = 'Rejected'
    else:
        pred = "Approved"

    return {"loan approval status" : pred}

