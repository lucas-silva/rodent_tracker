FROM gitpod/workspace-full-vnc

RUN sudo apt-get update  && sudo apt-get install -y ffmpeg libsm6 libxext6  && sudo rm -rf /var/lib/apt/lists/*