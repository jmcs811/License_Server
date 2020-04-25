from flask_restful import Resource, request
from flask import jsonify
import json
from common.utils import checkInfo

class Verify(Resource):
    def post(self):
        # convert string to json
        json_data = eval(request.data.decode()[:-1])
        if not request.is_json:
            return jsonify({"msg":"Missing JSON in request"})

        user_secret = json_data.get('secret', None)
        user_key = json_data.get('key', None)
        user_hwid = json_data.get('hwid', None)

        return checkInfo(user_key, user_hwid, user_secret)
