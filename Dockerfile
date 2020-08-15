FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        python3 \
        python3-pip \
        python3-tk \
        ghostscript \
        libgl1-mesa-dev \
        libglib2.0-0 \
    && pip3 install \
        camelot-py[cv]
