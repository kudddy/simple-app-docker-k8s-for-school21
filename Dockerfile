FROM python:3.6

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y -qq git python-dev libxml2-dev libxslt1-dev antiword \
                              unrtf poppler-utils tesseract-ocr flac \
                              ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig \
                              pkg-config libpoppler-private-dev libpoppler-cpp-dev\
    && apt-get clean

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
CMD python3 main.py