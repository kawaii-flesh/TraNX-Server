def get_translator(translator_type="google"):
    if translator_type == "google":
        from .google_translator import GoogleWebTranslator
        return GoogleWebTranslator()
    elif translator_type == "nllb":
        try:
            from .nllb_translator import NLLBTranslator
            return NLLBTranslator()
        except ImportError:
            raise ImportError("NLLB dependencies not installed. Run: pip install transformers torch")
    else:
        raise ValueError(f"Unsupported translator: {translator_type}")