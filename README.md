# NeoWhisper

NeoWhisper is a speech-to-text tool that is inspired by the [SuperWhisper](https://superwhisper.com) project.

> [!warning]
> 🚧 This work is currently a work in progress!

## Python Installation

> [!note]
> This project uses Python `3.14`.

### Ubuntu/Debian

```shell
sudo apt install python3.14 python3.14-venv
```

## Dependencies & Requirements Installation

### Ubuntu/Debian

```shell
# System Update
sudo apt update

# Install Python and Development Tools
sudo apt install -y \
    python3.14-dev \
    build-essential \
    portaudio19-dev

# Optional: NVIDIA GPU Support
sudo apt install -y nvidia-cuda-toolkit

# Create Virtual Environment
python3.14 -m venv .venv

# Activate Virtual Environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python Libraries
pip install -r requirements.txt
```
