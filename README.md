# TraNX-Server

TraNX-Server - OCR + перевод для экранного переводчика [TraNX](https://github.com/kawaii-flesh/TraNX)

## Устновка и запуск

### Windows + Google Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
pip install googletrans==4.0.0-rc1
python server.py --translator google
```

### Windows + Baidu Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Setup**:
  1.  **Get Baidu API Credentials**:
      Obtain an `APP_ID` and `APP_KEY` from the [Baidu Translate API Console](https://fanyi-api.baidu.com/manage/developer).

  2.  **Set Environment Variables**:
      You **MUST** set the following environment variables with your Baidu API credentials:
      - `BAIDU_TRANSLATOR_APP_ID="YOUR_APP_ID"`
      - `BAIDU_TRANSLATOR_APP_KEY="YOUR_APP_KEY"`
      Replace `"YOUR_APP_ID"` and `"YOUR_APP_KEY"` with your actual credentials.

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
python server.py --translator baidu
```

### Windows + Aliyun Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Setup**:
  1.  **Get Aliyun API Credentials**:
      Obtain an `ACCESS_KEY_ID` and `ACCESS_KEY_SECRET` from the [Aliyun RAM Console](https://ram.console.aliyun.com/).

  2.  **Set Environment Variables**:
      You **MUST** set the following environment variables with your Aliyun API credentials:
      - `ALIYUN_TRANSLATOR_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"`
      - `ALIYUN_TRANSLATOR_ACCESS_KEY_SECRET="YOUR_ACCESS_KEY_SECRET"`
      Replace `"YOUR_ACCESS_KEY_ID"` and `"YOUR_ACCESS_KEY_SECRET"` with your actual credentials.

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
pip install alibabacloud-alimt20181012
python server.py --translator aliyun
```

### Windows + Tencent Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Setup**:
  1.  **Get Tencent API Credentials**:
      Obtain a `SECRET_ID` and `SECRET_KEY` from the [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi).

  2.  **Set Environment Variables**:
      You **MUST** set the following environment variables with your Tencent API credentials:
      - `TENCENT_TRANSLATOR_SECRET_ID="YOUR_SECRET_ID"`
      - `TENCENT_TRANSLATOR_SECRET_KEY="YOUR_SECRET_KEY"`
      Replace `"YOUR_SECRET_ID"` and `"YOUR_SECRET_KEY"` with your actual credentials.

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
pip install tencentcloud-sdk-python
python server.py --translator tencent
```

### Windows + Youdao Translate

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **Setup**:
  1.  **Get Youdao API Credentials**:
      Obtain an `APP_KEY` and `APP_SECRET` from the [Youdao AI Platform](https://ai.youdao.com/console/#/service-provision/text-translation).

  2.  **Set Environment Variables**:
      You **MUST** set the following environment variables with your Youdao API credentials:
      - `YOUDAO_TRANSLATOR_APP_KEY="YOUR_APP_KEY"`
      - `YOUDAO_TRANSLATOR_APP_SECRET="YOUR_APP_SECRET"`
      Replace `"YOUR_APP_KEY"` and `"YOUR_APP_SECRET"` with your actual credentials.

```powershell
python -m venv tranx-venv
tranx-venv\Scripts\activate
pip install paddlepaddle==2.6.2 -f https://www.paddlepaddle.org.cn/whl/windows/cpu-mkl-avx/stable.html
pip install paddleocr==2.10.0
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
python server.py --translator youdao
```

### Windows + NLLB + Nvidia

Тестировалось с NVIDIA GeForce RTX 4060 Ti (8188MiB)

Если у вас недостаточно памяти для разворачивания модели [facebook/nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B), то попробуйте [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) указав ее в [tnx_translator/nllb_translator.py](https://github.com/kawaii-flesh/TraNX-Server/blob/main/tnx_translator/nllb_translator.py) -> `model_name`

Если вы обладаете большей памятью, то поробуйте [facebook/nllb-200-3.3B](https://huggingface.co/facebook/nllb-200-3.3B)

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
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
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
pip install flask==3.1.0 pillow==11.0.0 opencv-python==4.11.0.86 sentencepiece==0.2.0 protobuf==6.30.2 requests==2.32.3 symspellpy==6.9.0
python server.py --translator nllb
```

## Использование веб-конфигуратора

После запуска сервера на корневом URL будет доступен веб интерфейс для управления параметрами обработки изображения, OCR, переводчика

После первого запроса `TraNX` будет создан конфигурационный файл для конкретного тайтла, а также скрин — на примере которого можно настроить обработку изображения

![WEB-Configurator](/screenshots/web-config.png)
