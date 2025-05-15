import requests
import json
import time
import uuid
import hashlib
from typing import List, Dict
from .translator_interface import Translator

class YoudaoTranslator(Translator):
    YOUDAO_LANG_MAP = {
        'eng': 'en',
        'fra': 'fr',
        'deu': 'de',
        'jpn': 'ja',
        'kor': 'ko',
        'rus': 'ru',
        'zho': 'zh-CHS',
        'ukr': 'uk'
    }

    def __init__(self, app_key: str = None, app_secret: str = None):
        """
        Initialize the Youdao Translator.
        :param app_key: Your Youdao Translate API App Key.
        :param app_secret: Your Youdao Translate API App Secret.
        """
        if not app_key or not app_secret:
            raise ValueError("Youdao App Key and App Secret are required. Please provide them in the configuration.")
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_url = 'https://openapi.youdao.com/api'
        print(">>> Youdao Translate initialized. Ensure App Key and App Secret are correctly set.")

    def _generate_sign(self, query: str, salt: str, timestamp: str) -> str:
        # 有道API签名生成
        # 计算input长度
        input_len = len(query)
        # 根据有道API规则，如果input长度大于20，则计算前10个字符+长度+后10个字符的哈希
        # 否则直接计算input的哈希
        if input_len <= 20:
            input_md5 = query
        else:
            input_md5 = query[:10] + str(input_len) + query[-10:]
        
        # 拼接签名原文
        sign_str = self.app_key + input_md5 + salt + timestamp + self.app_secret
        # 计算签名
        sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
        return sign

    def translate(self, sentences: List[str], src_lang: str, dest_lang: str) -> List[str]:
        if not sentences:
            return []

        translated_sentences = []

        for sentence in sentences:
            if not sentence.strip():
                translated_sentences.append("")
                continue

            salt = str(uuid.uuid4())
            timestamp = str(int(time.time()))
            sign = self._generate_sign(sentence, salt, timestamp)

            params = {
                'q': sentence,
                'from': src_lang,
                'to': dest_lang,
                'appKey': self.app_key,
                'salt': salt,
                'sign': sign,
                'signType': 'v3',
                'curtime': timestamp
            }

            try:
                response = requests.get(self.api_url, params=params)
                response.raise_for_status()
                result = response.json()

                if 'translation' in result and result['translation']:
                    translated_text = " ".join(result['translation'])
                    translated_sentences.append(translated_text)
                elif 'errorCode' in result and result['errorCode'] != '0':
                    print(f"Youdao API Error: {result.get('errorCode')} - {result.get('msg', 'Unknown error')}")
                    translated_sentences.append(sentence)  # Return original sentence on error
                else:
                    print(f"Youdao API Error: Unexpected response format: {result}")
                    translated_sentences.append(sentence)

            except requests.exceptions.RequestException as e:
                print(f"Translation error (Youdao HTTP): {e}")
                translated_sentences.append(sentence)
            except json.JSONDecodeError as e:
                print(f"Translation error (Youdao JSON Decode): {e} - Response: {response.text}")
                translated_sentences.append(sentence)
            except Exception as e:
                print(f"Translation error (Youdao): {e}")
                translated_sentences.append(sentence)
        
        return translated_sentences

    def get_lang_map(self) -> Dict[str, str]:
        return self.YOUDAO_LANG_MAP