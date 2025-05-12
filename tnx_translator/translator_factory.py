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
    elif translator_type == "baidu":
        import os
        from .baidu_translator import BaiduTranslator
        app_id = os.environ.get("BAIDU_TRANSLATOR_APP_ID")
        app_key = os.environ.get("BAIDU_TRANSLATOR_APP_KEY")
        if not app_id or not app_key:
            raise ValueError(
                "Baidu App ID (BAIDU_TRANSLATOR_APP_ID) and App Key (BAIDU_TRANSLATOR_APP_KEY) must be set as environment variables. "
                "Please refer to the README.md for instructions on how to set them up."
            )
        return BaiduTranslator(app_id=app_id, app_key=app_key)
    else:
        raise ValueError(f"Unsupported translator: {translator_type}")