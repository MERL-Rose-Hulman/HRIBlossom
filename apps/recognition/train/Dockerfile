FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  libgl1 \
  libglib2.0-0 \
  git \
  && rm -rf /var/lib/apt/lists/*

# Install MediaPipe Model Maker
RUN pip install --upgrade pip
RUN pip install mediapipe-model-maker==0.2.1.4 tensorflow==2.15.0 matplotlib==3.7.2

WORKDIR /workspace

# Simple training script
COPY simple_train.py /workspace/

CMD ["python", "simple_train.py"]
