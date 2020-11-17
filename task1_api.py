import sys
import sklearn
import pickle
import xgboost as xgb
import json
import numpy as np
import spacy

def createVector(x):
    x = json.loads(x)
    # x will be a dict consisting of all the features along with the entry
    
    return person

def getPrediction(vector):
    pass

print("Ready for loading flask..")

app = Flask(__name__) 
api = Api(app) 
    
class test(Resource): 
  
    def get(self, value):         
        person_vector = createVector(value)
        regression_score = getPrediction(person_vector)
        return jsonify({'prediction_score': regression_score})                                                                                

# adding the defined resources along with their corresponding urls 
api.add_resource(test, '/test/<path:value>',methods=['GET']) 
  
# driver function 
if __name__ == '__main__': 
    print("Starting flask app..")
    app.run(host='0.0.0.0', debug=True,port=5000)