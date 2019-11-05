import os, requests, uuid, json

subscription_key = '32f1cb9c935a4cd4b33825e2869bff0f'

def get_translation(text_input, language_output="zh-Hans"):
    if not text_input:
        return ""
    
    # 去除pdf格式所造成的换行问题
    text_input = text_input.split("\n")
    text = ""
    new_begin = True
    length = len(text_input[0]) - 10
    for line in text_input:
        last_line = len(line) < length
        text += ((not new_begin) * " " + line.rstrip("-") + "\n" * last_line)
        new_begin = last_line or line[-1] == "-"
    text_input = text

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
