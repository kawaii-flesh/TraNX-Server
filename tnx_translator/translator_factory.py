def get_translator(translator_type="google"):
    if translator_type == "google":
        from .google_translator import GoogleWebTranslator

        return GoogleWebTranslator()
    elif translator_type == "nllb":
        try:
            from .nllb_translator import NLLBTranslator

            return NLLBTranslator()
        except ImportError:
            raise ImportError(
                "NLLB dependencies not installed. Run: pip install transformers torch"
            )
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
    elif translator_type == "aliyun":
        import os
        from .aliyun_translator import AliyunTranslator

        access_key_id = os.environ.get("ALIYUN_TRANSLATOR_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIYUN_TRANSLATOR_ACCESS_KEY_SECRET")
        if not access_key_id or not access_key_secret:
            raise ValueError(
                "Aliyun Access Key ID (ALIYUN_TRANSLATOR_ACCESS_KEY_ID) and Access Key Secret (ALIYUN_TRANSLATOR_ACCESS_KEY_SECRET) "
                "must be set as environment variables. Please refer to the README.md for instructions on how to set them up."
            )
        return AliyunTranslator(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )

    elif translator_type == "tencent":
        import os
        from .tencent_translator import TencentTranslator

        secret_id = os.environ.get("TENCENT_TRANSLATOR_SECRET_ID")
        secret_key = os.environ.get("TENCENT_TRANSLATOR_SECRET_KEY")
        if not secret_id or not secret_key:
            raise ValueError(
                "Tencent Secret ID (TENCENT_TRANSLATOR_SECRET_ID) and Secret Key (TENCENT_TRANSLATOR_SECRET_KEY) "
                "must be set as environment variables. Please refer to the README.md for instructions on how to set them up."
            )
        return TencentTranslator(secret_id=secret_id, secret_key=secret_key)

    elif translator_type == "youdao":
        import os
        from .youdao_translator import YoudaoTranslator

        app_key = os.environ.get("YOUDAO_TRANSLATOR_APP_KEY")
        app_secret = os.environ.get("YOUDAO_TRANSLATOR_APP_SECRET")
        if not app_key or not app_secret:
            raise ValueError(
                "Youdao App Key (YOUDAO_TRANSLATOR_APP_KEY) and App Secret (YOUDAO_TRANSLATOR_APP_SECRET) "
                "must be set as environment variables. Please refer to the README.md for instructions on how to set them up."
            )
        return YoudaoTranslator(app_key=app_key, app_secret=app_secret)
    else:
        raise ValueError(f"Unsupported translator: {translator_type}")
