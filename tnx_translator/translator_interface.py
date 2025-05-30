from abc import ABC, abstractmethod
from typing import List, Dict


class Translator(ABC):
    @abstractmethod
    def translate(
        self, sentences: List[str], src_lang: str, dest_lang: str
    ) -> List[str]:
        pass

    @abstractmethod
    def get_lang_map(self) -> Dict[str, str]:
        pass

    def convert_lang_code(self, lang_code: str, lang_codes: List[str]) -> str:
        lang_map = self.get_lang_map()
        for code in lang_codes:
            if code not in lang_map:
                raise ValueError(f"Unsupported language code: {code}")
        return lang_map[lang_code]
