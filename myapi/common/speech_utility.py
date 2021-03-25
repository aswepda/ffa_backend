from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from random import randrange



def text_to_speech(text):
    # bereits verwendet:
    #url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/8f767ae7-66ed-4222-b423-2482e0a25c1f'
    #apikey = 'g72_X_bSr5ksN4E2InJaiRyqBqd_smmmekD59y8iS_0q'
    
    #url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/063159ce-b301-432b-9913-593087aecf25'
    #apikey = 'GJyCioYwg1JzFe6hfzWl5lAa4bGJS3mDXDF3OfNQM4cS'


    rand_num = randrange(10)
    if rand_num == 0:
        url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/8a03fc07-4263-44fc-907d-2ede1c49562b'
        apikey = 'MUdicP3c-yaJz4PY-jkTj4dRwhOUS4LCU61BcEHN-04m' 
    elif rand_num == 1:
        url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/c0d4c11d-0239-4d76-9b72-5d615736ff50'
        apikey = 'hb22lwrAWwF1dBTx8N8aOSr0gtu2dZjj_RwMI07Ykh5E'
    elif rand_num == 2:
        url = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/54987379-4f29-4614-b000-266db5d4f11e'
        apikey = 'DDmm-ef5J_KcAzblvUo4CQ9lVKhLAZd_eG0fO3jg7SnY'
    elif rand_num == 3:
        url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/97591f7f-5d59-4e8f-bb21-301f5c5e2000'
        apikey = 'KPX_dnUwbjZZeBvLwWTx3p9-cLyAd5rv4spjZ2Sa1942'
    elif rand_num == 4:
        url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/8e4b452c-240f-432f-a6db-cf75e9a78926'
        apikey = 'Xl7m-tQOKxi_y0FkoQDUhXTcWjJwP8GcRKkTakeZ6bz3'

    # Setup Service
    authenticator = IAMAuthenticator(apikey)
    # New TTS Service
    tts = TextToSpeechV1(authenticator=authenticator)
    # Set Service URL
    tts.set_service_url(url)

    return tts.synthesize(text, accept='audio/mp3', voice='de-DE_BirgitV3Voice').get_result().content
        