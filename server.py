from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from flask import make_response
import json

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True

@app.route('/')
def something():
  response=make_response("Hey there!", 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

if __name__ == '__main__':
    app.run()
