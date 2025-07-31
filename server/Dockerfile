FROM python:3.11-slim 

WORKDIR /app 
COPY . . 

# Install system deps for audio, ffmpeg, and build tools
RUN apt-get update && apt-get install -y \
    ffmpeg libgl1-mesa-glx git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* 

# Install Rust (needed for some Python packages)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip
RUN pip install -r requirements-py311.txt

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]