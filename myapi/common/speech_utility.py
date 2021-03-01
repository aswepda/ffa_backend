from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def text_to_speech(text):
    url = 'https://api.eu-de.text-to-speech.watson.cloud.ibm.com/instances/8f767ae7-66ed-4222-b423-2482e0a25c1f'
    apikey = 'g72_X_bSr5ksN4E2InJaiRyqBqd_smmmekD59y8iS_0q'

    # Setup Service
    authenticator = IAMAuthenticator(apikey)
    # New TTS Service
    tts = TextToSpeechV1(authenticator=authenticator)
    # Set Service URL
    tts.set_service_url(url)

    return tts.synthesize(text, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result().content
        