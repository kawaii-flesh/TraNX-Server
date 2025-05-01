import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from .translator_interface import Translator
from typing import List, Dict

class NLLBTranslator(Translator):
    NLLB_LANG_MAP = {
        'eng': 'eng_Latn',
        'fra': 'fra_Latn',
        'deu': 'deu_Latn',
        'jpn': 'jpn_Jpan',
        'kor': 'kor_Hang',
        'rus': 'rus_Cyrl',
        'zho': 'zho_Hans',
        'ukr': 'ukr_Cyrl'
    }
    def __init__(self, model_name="facebook/nllb-200-1.3B"):
        self.device = 0 if torch.cuda.is_available() else -1
        print(">>> Loading NLLB translation model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        if self.device == 0:
            self.model.to('cuda')

    def translate(self, sentences: List[str], src_lang: str, dest_lang: str) -> List[str]:
        try:
            translated_sentences = []
            for sentence in sentences:
                inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
                if self.device == 0:
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                forced_token = self.tokenizer._convert_token_to_id_with_added_voc(dest_lang)
                output = self.model.generate(**inputs, forced_bos_token_id=forced_token, max_new_tokens=512, num_beams=4)
                translated = self.tokenizer.decode(output[0], skip_special_tokens=True)
                translated_sentences.append(translated)
            return translated_sentences
        except Exception as e:
            print(f"Translation error (NLLB): {e}")
            return sentences

    def get_lang_map(self) -> Dict[str, str]:
        return self.NLLB_LANG_MAP