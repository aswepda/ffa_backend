from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def text_to_speech(text):
    #url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/8f767ae7-66ed-4222-b423-2482e0a25c1f'
    #apikey = 'g72_X_bSr5ksN4E2InJaiRyqBqd_smmmekD59y8iS_0q'
    url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/063159ce-b301-432b-9913-593087aecf25'
    apikey = 'GJyCioYwg1JzFe6hfzWl5lAa4bGJS3mDXDF3OfNQM4cS'
    
    # Setup Service
    authenticator = IAMAuthenticator(apikey)
    # New TTS Service
    tts = TextToSpeechV1(authenticator=authenticator)
    # Set Service URL
    tts.set_service_url(url)

    return tts.synthesize(text, accept='audio/mp3', voice='de-DE_BirgitV3Voice').get_result().content
        