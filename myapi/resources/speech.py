from flask_restful import Resource, abort, request

import base64
import common.speech_utility 

class Speech(Resource):
    def get(self):
        args = request.args
        
        if "text" not in request.args:
            return abort(400, message='Wrong query param')

        var = common.speech_utility.text_to_speech(args['text'])
        
        return {"speech":str(base64.b64encode(var), 'ascii', 'ignore')}
        