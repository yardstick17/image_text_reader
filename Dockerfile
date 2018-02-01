FROM tleyden5iwx/open-ocr-2
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /home/

RUN set -eux \
    && apt-get update \
    && apt-get install -y python3-pip python-dev build-essential \
    && apt install -y libsm6 libxext6

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

ADD . /home

CMD ["bash"]
