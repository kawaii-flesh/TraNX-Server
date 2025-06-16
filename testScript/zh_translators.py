import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tnx_translator.baidu_translator import BaiduTranslator
from tnx_translator.tencent_translator import TencentTranslator
from tnx_translator.aliyun_translator import AliyunTranslator
from tnx_translator.youdao_translator import YoudaoTranslator


def test_baidu():
    print("Baidu Translator Test")
    print("---------------------")

    app_id = input("Please input Baidu App ID: ")
    app_key = input("Please input Baidu App Key: ")

    if not app_id or not app_key:
        print("Error：App ID or App Key is empty.")
        return

    try:
        translator = BaiduTranslator(app_id=app_id, app_key=app_key)
    except ValueError as e:
        print(f"init error: {e}")
        return

    print("---------------------")
    sentence_to_translate = input("Please input the sentence to translate: ")
    source_lang = input(
        "Please input the source language code (e.g., 'en' for English, 'zh' for Chinese): "
    )
    destination_lang = input(
        "Please input the destination language code (e.g., 'zh' for Chinese, 'en' for English): "
    )

    if not sentence_to_translate.strip():
        print("Error: Sentence to translate is empty.")
        return

    if not source_lang or not destination_lang:
        print("Error: Source or destination language code is empty.")
        return

    print("\ntranslating...")
    try:
        translated_sentences = translator.translate(
            sentence_to_translate, source_lang, destination_lang
        )
        if translated_sentences:
            print(f"result: {translated_sentences}")
        else:
            print("translation failed.")
    except Exception as e:
        print(f"translation err {e}")


def test_tencent():
    print("Tencent Translator Test")
    print("---------------------")

    secret_id = input("Please input Tencent Secret ID: ")
    secret_key = input("Please input Tencent Secret Key: ")

    if not secret_id or not secret_key:
        print("Error：Secret ID or Secret Key is empty.")
        return

    try:
        translator = TencentTranslator(secret_id=secret_id, secret_key=secret_key)
    except ValueError as e:
        print(f"init error: {e}")
        return

    print("---------------------")
    sentence_to_translate = input("Please input the sentence to translate: ")
    source_lang = input(
        "Please input the source language code (e.g., 'en' for English, 'zh' for Chinese): "
    )
    destination_lang = input(
        "Please input the destination language code (e.g., 'zh' for Chinese, 'en' for English): "
    )

    if not sentence_to_translate.strip():
        print("Error: Sentence to translate is empty.")
        return

    if not source_lang or not destination_lang:
        print("Error: Source or destination language code is empty.")
        return

    print("\ntranslating...")
    try:
        translated_sentences = translator.translate(
            sentence_to_translate, source_lang, destination_lang
        )
        if translated_sentences:
            print(f"result: {translated_sentences}")
        else:
            print("translation failed.")
    except Exception as e:
        print(f"translation err {e}")


def test_aliyun():
    print("Aliyun Translator Test")
    print("---------------------")

    access_key_id = input("Please input Aliyun Access Key ID: ")
    access_key_secret = input("Please input Aliyun Access Key Secret: ")

    if not access_key_id or not access_key_secret:
        print("Error：Access Key ID or Access Key Secret is empty.")
        return

    try:
        translator = AliyunTranslator(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )
    except ValueError as e:
        print(f"init error: {e}")
        return

    print("---------------------")
    sentence_to_translate = input("Please input the sentence to translate: ")
    source_lang = input(
        "Please input the source language code (e.g., 'en' for English, 'zh' for Chinese): "
    )
    destination_lang = input(
        "Please input the destination language code (e.g., 'zh' for Chinese, 'en' for English): "
    )

    if not sentence_to_translate.strip():
        print("Error: Sentence to translate is empty.")
        return

    if not source_lang or not destination_lang:
        print("Error: Source or destination language code is empty.")
        return

    print("\ntranslating...")
    try:
        translated_sentences = translator.translate(
            sentence_to_translate, source_lang, destination_lang
        )
        if translated_sentences:
            print(f"result: {translated_sentences}")
        else:
            print("translation failed.")
    except Exception as e:
        print(f"translation err {e}")


def test_youdao():
    print("Youdao Translator Test")
    print("---------------------")

    app_key = input("Please input Youdao App Key: ")
    app_secret = input("Please input Youdao App Secret: ")

    if not app_key or not app_secret:
        print("Error：App Key or App Secret is empty.")
        return

    try:
        translator = YoudaoTranslator(app_key=app_key, app_secret=app_secret)
    except ValueError as e:
        print(f"init error: {e}")
        return

    print("---------------------")
    sentence_to_translate = input("Please input the sentence to translate: ")
    source_lang = input(
        "Please input the source language code (e.g., 'en' for English, 'zh' for Chinese): "
    )
    destination_lang = input(
        "Please input the destination language code (e.g., 'zh' for Chinese, 'en' for English): "
    )

    if not sentence_to_translate.strip():
        print("Error: Sentence to translate is empty.")
        return

    if not source_lang or not destination_lang:
        print("Error: Source or destination language code is empty.")
        return

    print("\ntranslating...")
    try:
        translated_sentences = translator.translate(
            sentence_to_translate, source_lang, destination_lang
        )
        if translated_sentences:
            print(f"result: {translated_sentences}")
        else:
            print("translation failed.")
    except Exception as e:
        print(f"translation err {e}")


def main():
    print("Translator Test Program")
    print("=======================")
    print("1. Test Baidu Translator")
    print("2. Test Tencent Translator")
    print("3. Test Aliyun Translator")
    print("4. Test Youdao Translator")
    print("0. Exit")

    choice = input("\nPlease select a translator to test (0-4): ")

    if choice == "1":
        test_baidu()
    elif choice == "2":
        test_tencent()
    elif choice == "3":
        test_aliyun()
    elif choice == "4":
        test_youdao()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
