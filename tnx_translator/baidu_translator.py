import requests
import random
import json
from hashlib import md5
from typing import List, Dict
from .translator_interface import Translator

class BaiduTranslator(Translator):
    BAIDU_LANG_MAP = {
        'eng': 'en',
        'fra': 'fra',
        'deu': 'de',
        'jpn': 'jp',
        'kor': 'kor',
        'rus': 'ru',
        'zho': 'zh',
        'ukr': 'ukr'
    }

    def __init__(self, app_id: str = None, app_key: str = None):
        """
        Initialize the Baidu Translator.
        :param app_id: Your Baidu Translate API App ID.
        :param app_key: Your Baidu Translate API App Key.
        """
        if not app_id or not app_key:
            raise ValueError("Baidu App ID and App Key are required. Please provide them in the configuration.")
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        print(">>> Baidu Translate initialized. Ensure APP_ID and APP_KEY are correctly set.")

    def _make_sign(self, query: str, salt: str) -> str:
        sign_str = self.app_id + query + salt + self.app_key
        return md5(sign_str.encode('utf-8')).hexdigest()

    def translate(self, sentences: List[str], src_lang: str, dest_lang: str) -> List[str]:
        if not sentences:
            return []

        translated_sentences = []
        # Baidu API seems to prefer single query for batch, but we process sentence by sentence for consistency
        # and to handle potential individual sentence errors more gracefully.
        # If Baidu API supports batch translation in a single request, this can be optimized.

        for sentence in sentences:
            if not sentence.strip():
                translated_sentences.append("")
                continue

            salt = str(random.randint(32768, 65536))
            sign = self._make_sign(sentence, salt)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                'q': sentence,
                'from': self.BAIDU_LANG_MAP.get(src_lang, 'auto'), # Use 'auto' if src_lang not in map
                'to': self.BAIDU_LANG_MAP.get(dest_lang, dest_lang),
                'appid': self.app_id,
                'salt': salt,
                'sign': sign
            }

            try:
                response = requests.post(self.api_url, params=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = response.json()

                if 'trans_result' in result:
                    translated_text = " ".join([item['dst'] for item in result['trans_result']])
                    translated_sentences.append(translated_text)
                elif 'error_code' in result:
                    print(f"Baidu API Error: {result['error_code']} - {result.get('error_msg', 'Unknown error')}")
                    translated_sentences.append(sentence) # Return original sentence on error
                else:
                    print(f"Baidu API Error: Unexpected response format: {result}")
                    translated_sentences.append(sentence)

            except requests.exceptions.RequestException as e:
                print(f"Translation error (Baidu HTTP): {e}")
                translated_sentences.append(sentence)
            except json.JSONDecodeError as e:
                print(f"Translation error (Baidu JSON Decode): {e} - Response: {response.text}")
                translated_sentences.append(sentence)
            except Exception as e:
                print(f"Translation error (Baidu): {e}")
                translated_sentences.append(sentence)
        
        return translated_sentences

    def get_lang_map(self) -> Dict[str, str]:
        return self.BAIDU_LANG_MAP
