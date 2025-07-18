from typing import List, Dict
from alibabacloud_alimt20181012.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_alimt20181012.models import TranslateGeneralRequest
from alibabacloud_tea_util.models import RuntimeOptions
from .translator_interface import Translator


class AliyunTranslator(Translator):
    def __init__(self, access_key_id: str, access_key_secret: str):
        """Initialize Aliyun translator with credentials

        Args:
            access_key_id (str): Aliyun access key ID
            access_key_secret (str): Aliyun access key secret
        """
        config = Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint="mt.cn-hangzhou.aliyuncs.com",
        )
        self.client = Client(config)

    ALIYUN_LANG_MAP = {
        "eng": "en",
        "fra": "fr",
        "deu": "de",
        "jpn": "ja",
        "kor": "ko",
        "rus": "ru",
        "zho": "zh",
        "zht": "zh-tw",
        "ukr": "ru",  # Aliyun doesn't support Ukrainian, fallback to Russian
    }

    def translate(self, sentence: str, src_lang: str, dest_lang: str) -> str:
        """Translate a sentence from source language to target language

        Args:
            sentence (str): Sentence to translate
            src_lang (str): Source language code
            dest_lang (str): Target language code

        Returns:
            str: Translated sentence

        Raises:
            ValueError: If language code is not supported
            Exception: If translation fails with API error
        """
        try:
            # Prepare request
            runtime = RuntimeOptions()

            # Translate sentence
            request = TranslateGeneralRequest(
                source_language=src_lang,
                target_language=dest_lang,
                source_text=sentence,
                format_type="text",
                scene="general",
            )

            # Call API
            response = self.client.translate_general_with_options(request, runtime)

            # Handle both possible response structures
            try:
                translated = ""
                if hasattr(response.body, "code"):
                    code = response.body.code
                    message = response.body.message
                    translated = response.body.data.translated
                else:
                    code = response.body.Code
                    message = response.body.Message
                    translated = response.body.Data.Translated

                if code != "200":
                    raise Exception(
                        f"Translation failed with code {code}: {message}\nFull response: {response}"
                    )
                
                return translated

            except AttributeError as e:
                raise Exception(
                    f"Unexpected response structure: {str(e)}\nFull response: {response}"
                )

        except ValueError as e:
            raise ValueError(f"Language code error: {str(e)}")
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")

        return sentence  # Return original sentence on error

    def get_lang_map(self) -> Dict[str, str]:
        """Get the language code mapping

        Returns:
            Dict[str, str]: Dictionary mapping standard codes to Aliyun codes
        """
        return self.ALIYUN_LANG_MAP
