from flask_restful import Resource
from flask_restful import request

import base64
import common.speech_utility 

class Speech(Resource):
    def get(self):
        args = request.args
        var = common.speech_utility.text_to_speech(str(args))
        
        return {"speech":str(base64.b64encode(var), 'ascii', 'ignore')}
        