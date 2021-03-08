import common.speech_utility 
import base64

def test_connection():
    var = str(base64.b64encode(common.speech_utility.text_to_speech("test")), 'ascii', 'ignore')
    assert var.startswith("SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//")


        