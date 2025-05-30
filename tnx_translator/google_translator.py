from googletrans import Translator as GoogleTranslator
from .translator_interface import Translator
from typing import List, Dict

class GoogleWebTranslator(Translator):
    # https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages
    GOOGLE_LANG_MAP = {
        'eng': 'en',
        'fra': 'fr',
        'deu': 'de', 
        'jpn': 'ja',
        'kor': 'ko',
        'rus': 'ru',
        'zho': 'zh-cn',
        'ukr': 'uk',
        'zht': 'zh-tw'
    }

    def __init__(self):
        self.translator = GoogleTranslator()
        print(">>> Google Translate ready")

    def translate(self, sentences: List[str], src_lang: str, dest_lang: str) -> List[str]:
        translated_sentences = []
        try:
            for sentence in sentences:
                result = self.translator.translate(sentence, src=src_lang, dest=dest_lang)
                translated_sentences.append(result.text.replace(" -", "-"))
            return translated_sentences
        except Exception as e:
            print(f"Translation error (Google): {e}")
            return sentences

    def get_lang_map(self) -> Dict[str, str]:
        return self.GOOGLE_LANG_MAP