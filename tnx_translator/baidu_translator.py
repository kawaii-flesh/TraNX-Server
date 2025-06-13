import requests
import random
import json
from hashlib import md5
from typing import List, Dict
from .translator_interface import Translator


class BaiduTranslator(Translator):
    BAIDU_LANG_MAP = {
        "eng": "en",
        "fra": "fra",
        "deu": "de",
        "jpn": "jp",
        "kor": "kor",
        "rus": "ru",
        "zho": "zh",
        "zht": "cht",
        "ukr": "ukr",
    }

    def __init__(self, app_id: str = None, app_key: str = None):
        """
        Initialize the Baidu Translator.
        :param app_id: Your Baidu Translate API App ID.
        :param app_key: Your Baidu Translate API App Key.
        """
        if not app_id or not app_key:
            raise ValueError(
                "Baidu App ID and App Key are required. Please provide them in the configuration."
            )
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
        print(
            ">>> Baidu Translate initialized. Ensure APP_ID and APP_KEY are correctly set."
        )

    def _make_sign(self, query: str, salt: str) -> str:
        sign_str = self.app_id + query + salt + self.app_key
        return md5(sign_str.encode("utf-8")).hexdigest()

    def translate(self, sentence: str, src_lang: str, dest_lang: str) -> str:
        # Baidu API seems to prefer single query for batch, but we process sentence by sentence for consistency
        # and to handle potential individual sentence errors more gracefully.
        # If Baidu API supports batch translation in a single request, this can be optimized.

        salt = str(random.randint(32768, 65536))
        sign = self._make_sign(sentence, salt)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "q": sentence,
            "from": src_lang,
            "to": dest_lang,
            "appid": self.app_id,
            "salt": salt,
            "sign": sign,
        }

        try:
            response = requests.post(self.api_url, params=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()

            if "trans_result" in result:
                translated_text = " ".join(
                    [item["dst"] for item in result["trans_result"]]
                )
                return translated_text
            elif "error_code" in result:
                print(
                    f"Baidu API Error: {result['error_code']} - {result.get('error_msg', 'Unknown error')}"
                )
            else:
                print(f"Baidu API Error: Unexpected response format: {result}")

        except requests.exceptions.RequestException as e:
            print(f"Translation error (Baidu HTTP): {e}")
        except json.JSONDecodeError as e:
            print(
                f"Translation error (Baidu JSON Decode): {e} - Response: {response.text}"
            )
        except Exception as e:
            print(f"Translation error (Baidu): {e}")

        return sentence  # Return original sentence on error

    def get_lang_map(self) -> Dict[str, str]:
        return self.BAIDU_LANG_MAP
