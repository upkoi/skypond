FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
     && apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        g++  \
        git  \
        curl  \
        cmake \
        zlib1g-dev \
        libjpeg-dev \
        xvfb \
        libav-tools \
        xorg-dev \
        libboost-all-dev \
        libsdl2-dev \
        swig \
        python3  \
        python3-dev  \
        python3-future  \
        python3-pip  \
        python3-setuptools  \
        python3-wheel  \
        python3-tk \
        libopenblas-base  \
        libatlas-dev  \
        cython3  \
        nodejs  \
        ruby  \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y libssl-dev

RUN python3 -m pip install --upgrade pip

RUN pip install setuptools --upgrade

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN pip install https://download.pytorch.org/whl/cpu/torch-1.0.1.post2-cp35-cp35m-linux_x86_64.whl
RUN pip install torchvision==0.2.2.post3 torch-ac==1.0.2
RUN pip install Naked

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get -y install curl iptables sudo
RUN useradd -m app

COPY entry.sh /app/entry.sh

WORKDIR /app

COPY entry.sh /app
COPY skypond /app/skypond
RUN cd skypond && python3 setup.py install

RUN ["chmod", "+x", "/app/entry.sh"]

ENTRYPOINT ["/app/entry.sh", "--"]

CMD [ "python3 /mnt/agent/handler.py" ]
