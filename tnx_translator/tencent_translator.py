import requests
import hmac
import json
import time
import hashlib
from typing import List, Dict
from .translator_interface import Translator


class TencentTranslator(Translator):
    TENCENT_LANG_MAP = {
        "eng": "en",
        "fra": "fr",
        "deu": "de",
        "jpn": "ja",
        "kor": "ko",
        "rus": "ru",
        "zho": "zh",
        "zht": "zh-TW",
        "ukr": "uk",
    }

    def __init__(self, secret_id: str = None, secret_key: str = None):
        """
        Initialize the Tencent Translator.
        :param secret_id: Your Tencent Cloud Secret ID.
        :param secret_key: Your Tencent Cloud Secret Key.
        """
        if not secret_id or not secret_key:
            raise ValueError(
                "Tencent Secret ID and Secret Key are required. Please provide them in the configuration."
            )
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.api_url = "https://tmt.tencentcloudapi.com"
        print(
            ">>> Tencent Translate initialized. Ensure Secret ID and Secret Key are correctly set."
        )

    def _generate_sign(self, params: Dict[str, str], timestamp: int) -> str:
        # 腾讯云API签名生成
        service = "tmt"
        host = "tmt.tencentcloudapi.com"
        algorithm = "TC3-HMAC-SHA256"
        date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))

        # 1. 拼接规范请求串
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = f"content-type:{ct}\nhost:{host}\n"
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (
            f"{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n"
            f"{canonical_headers}\n{signed_headers}\n{hashed_request_payload}"
        )

        # 2. 拼接待签名字符串
        credential_scope = f"{date}/{service}/tc3_request"
        hashed_canonical_request = hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest()
        string_to_sign = (
            f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_canonical_request}"
        )

        # 3. 计算签名
        def _sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = _sign(("TC3" + self.secret_key).encode("utf-8"), date)
        secret_service = _sign(secret_date, service)
        secret_signing = _sign(secret_service, "tc3_request")
        signature = hmac.new(
            secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # 4. 拼接Authorization
        authorization = (
            f"{algorithm} Credential={self.secret_id}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )

        return authorization

    def translate(self, sentence: str, src_lang: str, dest_lang: str) -> str:
        timestamp = int(time.time())
        params = {
            "SourceText": sentence,
            "Source": src_lang,
            "Target": dest_lang,
            "ProjectId": 0,
        }

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Host": "tmt.tencentcloudapi.com",
            "X-TC-Action": "TextTranslate",
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": "2018-03-21",
            "X-TC-Region": "ap-guangzhou",
            "Authorization": self._generate_sign(params, timestamp),
        }

        try:
            response = requests.post(
                self.api_url, data=json.dumps(params), headers=headers
            )
            response.raise_for_status()
            result = response.json()

            if "Response" in result and "TargetText" in result["Response"]:
                return result["Response"]["TargetText"]
            elif "Response" in result and "Error" in result["Response"]:
                error = result["Response"]["Error"]
                print(
                    f"Tencent API Error: {error.get('Code')} - {error.get('Message', 'Unknown error')}"
                )
            else:
                print(f"Tencent API Error: Unexpected response format: {result}")

        except requests.exceptions.RequestException as e:
            print(f"Translation error (Tencent HTTP): {e}")
        except json.JSONDecodeError as e:
            print(
                f"Translation error (Tencent JSON Decode): {e} - Response: {response.text}"
            )
        except Exception as e:
            print(f"Translation error (Tencent): {e}")

        return sentence  # Return original sentence on error

    def get_lang_map(self) -> Dict[str, str]:
        return self.TENCENT_LANG_MAP
