# Import flask and datetime module for showing date and time
from flask import Flask
from flask_cors import CORS, cross_origin
import time
  
# Initializing flask app
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
  
# Route for seeing a data
@app.route('/time')
def fun():
  
    # Returning an api for showing in reactjs
    return {'time': time.time()}
  
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)