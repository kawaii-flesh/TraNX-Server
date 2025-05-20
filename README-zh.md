# TraNX-Server

TraNX-Server - 屏幕OCR翻译器，配套插件：[TraNX](https://github.com/kawaii-flesh/TraNX) 

Инструкции на русском языке: [README-zh.md](README-zh.md)

English Introduction: [README-en.md](README-en.md)

## 安装与启动

### Windows + 谷歌翻译

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

### Windows + 百度翻译

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **获取密钥**：
从 [百度翻译 API 控制台](https://fanyi-api.baidu.com/manage/developer) 获取 `APP_ID` 和 `APP_KEY`。

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

### Windows + 阿里云翻译

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **获取密钥**：
从 [阿里云 RAM 控制台](https://ram.console.aliyun.com/) 获取 `ACCESS_KEY_ID` 和 `ACCESS_KEY_SECRET`。

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

### Windows + 腾讯翻译

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **获取密钥**：
从 [腾讯云控制台](https://console.cloud.tencent.com/cam/capi) 获取 `SECRET_ID` 和 `SECRET_KEY`。

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

### Windows + 有道翻译

- [Python](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

- **获取密钥**：
从 [有道 AI 平台](https://ai.youdao.com/console/#/service-provision/text-translation) 获取 `APP_KEY` 和 `APP_SECRET`。

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

已在 NVIDIA GeForce RTX 4060 Ti (8188MiB) 上进行测试。

如果您的内存不足以部署 [facebook/nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B) 模型，可以尝试 [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M)，并在 [tnx_translator/nllb_translator.py](https://github.com/kawaii-flesh/TraNX-Server/blob/main/tnx_translator/nllb_translator.py) 中指定 `model_name`。

如果您有更多的内存，可以尝试 [facebook/nllb-200-3.3B](https://huggingface.co/facebook/nllb-200-3.3B)。

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

## 使用 Web 配置器

服务器启动后，在根 URL 上可以访问一个 Web 界面，用于管理图像、OCR 和翻译器的处理参数。

第一次请求 `TraNX` 后，将为特定标题创建一个配置文件，以及一个屏幕截图，可用于调整图像的处理。

![Web 配置器](/screenshots/web-config.png)

----------------------------------------------------
使用有道、腾讯、阿里云、百度翻译时，需要在 **Text Processing** 部分取消勾选 **Split Text into Sentences for Translation**。

![Web 配置器](/screenshots/web-config2.png)