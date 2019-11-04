import os, requests, uuid, json

subscription_key = '32f1cb9c935a4cd4b33825e2869bff0f'

def get_translation(text_input, language_output="zh-Hans"):
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + language_output
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'global',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text' : text_input
    }]
    response = requests.post(constructed_url, headers=headers, json=body)
    result = response.json()
    return result[0]['translations'][0]['text']
if __name__ == "__main__":
    result = get_translation("who is your daddy")
    print(type(result))
    print(result)
