import os, requests, uuid, json
from googletrans import Translator
from googletrans import urls, utils
from googletrans.compat import PY3
from googletrans.constants import DEFAULT_USER_AGENT
subscription_key = '32f1cb9c935a4cd4b33825e2869bff0f'

class MyTranslator(Translator):
    def __init__(self,service_urls=None, user_agent=DEFAULT_USER_AGENT,
                 proxies=None, timeout=None):
        super().__init__(service_urls,user_agent,proxies,timeout)

    def _translate(self, text, dest, src):
        if not PY3 and isinstance(text, str):  # pragma: nocover
            text = text.decode('utf-8')

        token = self.token_acquirer.do(text)
        params = utils.build_params(query=text, src=src, dest=dest,
                                    token=token)
        params['client'] = 'webapp'
        url = urls.TRANSLATE.format(host=self._pick_service_url())
        r = self.session.get(url, params=params)

        data = utils.format_json(r.text)
        return data

def get_translation_by_google(text_input):
    # # 去除pdf格式所造成的换行问题
    # text_input = text_input.split("\n")
    # text = ""
    # new_begin = True
    # length = len(text_input[0]) - 10
    # for line in text_input:
    #     last_line = len(line) < length
    #     text += ((not new_begin) * " " + line.rstrip("-") + "\n" * last_line)
    #     new_begin = last_line or line[-1] == "-"
    # text_input = text

    translator = MyTranslator(service_urls=["translate.google.cn"])
    translate_res = translator.translate(text_input, dest='zh-cn')
    return translate_res.text

def get_translation(text_input, language_output="zh-Hans"):
    if not text_input:
        return ""
    
    # # 去除pdf格式所造成的换行问题
    # text_input = text_input.split("\n")
    # text = ""
    # new_begin = True
    # length = len(text_input[0]) - 10
    # for line in text_input:
    #     last_line = len(line) < length
    #     text += ((not new_begin) * " " + line.rstrip("-") + "\n" * last_line)
    #     new_begin = last_line or line[-1] == "-"
    # text_input = text

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
