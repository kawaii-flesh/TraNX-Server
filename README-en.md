# TraNX-Server

TraNX-Server - OCR + translation for the screen translator [TraNX](https://github.com/kawaii-flesh/TraNX)

Инструкции на русском языке: [README.md](README.md)

中文说明: [README-zh.md](README-zh.md)

## Installation and Startup

### Windows + Google Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
pip install googletrans==4.0.0-rc1
python server.py --translator google
```

### Windows + Baidu Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Get Keys**:
Get `APP_ID` and `APP_KEY` from [Baidu Translate API Console](https://fanyi-api.baidu.com/manage/developer).

```cmd
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
set BAIDU_TRANSLATOR_APP_ID=APP_ID
set BAIDU_TRANSLATOR_APP_KEY=APP_KEY
python server.py --translator baidu
```

### Windows + Aliyun Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Get Keys**:
Get `ACCESS_KEY_ID` and `ACCESS_KEY_SECRET` from [Aliyun RAM Console](https://ram.console.aliyun.com/).

```cmd
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
pip install alibabacloud-alimt20181012==1.5.0
set ALIYUN_TRANSLATOR_ACCESS_KEY_ID=ACCESS_KEY_ID
set ALIYUN_TRANSLATOR_ACCESS_KEY_SECRET=ACCESS_KEY_SECRET
python server.py --translator aliyun
```

### Windows + Tencent Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Get Keys**:
Get `SECRET_ID` and `SECRET_KEY` from [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi).

```cmd
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
set TENCENT_TRANSLATOR_SECRET_ID=SECRET_ID
set TENCENT_TRANSLATOR_SECRET_KEY=SECRET_KEY
python server.py --translator tencent
```

### Windows + Youdao Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Get Keys**:
Get `APP_KEY` and `APP_SECRET` from [Youdao AI Platform](https://ai.youdao.com/console/#/service-provision/text-translation).

```cmd
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
set YOUDAO_TRANSLATOR_APP_KEY=APP_KEY
set YOUDAO_TRANSLATOR_APP_SECRET=APP_SECRET
python server.py --translator youdao
```

### Windows + NLLB + Nvidia

Tested with NVIDIA GeForce RTX 4060 Ti (8188MiB)

If you don't have enough memory to deploy the [facebook/nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B) model, try [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) by specifying it in [tnx_translator/nllb_translator.py](https://github.com/kawaii-flesh/TraNX-Server/blob/main/tnx_translator/nllb_translator.py) -> `model_name`

If you have more memory, try [facebook/nllb-200-3.3B](https://huggingface.co/facebook/nllb-200-3.3B)

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)
- [CUDA 11.8](https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe)
- [cuDNN 8.6](https://developer.nvidia.com/compute/cudnn/secure/8.6.0/local_installers/11.8/cudnn-windows-x86_64-8.6.0.163_cuda11-archive.zip)

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install numpy==1.26.4
pip install torch==2.2.2+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers==4.51.3
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
python server.py --translator nllb
```

### Windows + NLLB + CPU

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install numpy==1.26.4
pip install torch==2.2.2+cpu torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers==4.51.3
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==3.20.2 requests==2.32.3 symspellpy==6.9.0
python server.py --translator nllb
```

## Using the Web Configurator

After starting the server, a web interface will be available at the root URL for managing the image processing, OCR, and translator parameters.

After the first `TraNX` request, a configuration file will be created for a specific title, along with a screenshot, which can be used to adjust the image processing.

![WEB-Configurator](/screenshots/web-config.png)

----------------------------------------------------
When using Youdao, Tencent, Aliyun, or Baidu Translate, you need to uncheck the **Split text into sentences for translation** option in the **Text Processing** section.

![WEB-Configurator](/screenshots/web-config2.png)