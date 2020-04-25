from flask import Flask
from flask_restful import Resource, Api
from resources.verify import Verify

app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(Verify, '/api/verify')

if __name__ == '__main__':
    app.run(host='0.0.0.0')