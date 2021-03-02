from flask_restful import Resource

import base64
import common.speech_utility 

class Speech(Resource):
    def get(self):
        var = common.speech_utility.text_to_speech("test")
        
        return {"speech":str(base64.b64encode(var), 'ascii', 'ignore')}
        