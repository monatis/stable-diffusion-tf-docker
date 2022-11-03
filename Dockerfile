from tensorflow/tensorflow:2.10.0-gpu

RUN apt update && \
    apt install -y git && \
    pip install --no-cache-dir Pillow==9.2.0 tqdm==4.64.1 python-multipart \
    ftfy==6.1.1 regex==2022.9.13 tensorflow-addons==0.17.1 \
    fastapi "uvicorn[standard]" git+https://github.com/divamgupta/stable-diffusion-tensorflow.git

WORKDIR /app

COPY ./app.py /app/app.py

CMD uvicorn --host 0.0.0.0 app:app