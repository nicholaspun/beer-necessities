FROM python:3-stretch

RUN pip install -r requirements.txt

# TODO: Slim this down?
RUN python -m nltk.downloader -d /usr/local/share/nltk_data all

ADD senna-v3.0.tgz /senna

WORKDIR /beer-necessities

COPY scripts/ /beer-necessities/scripts
COPY app/ /beer-necessities/app

CMD [ "python", "csv_to_obj.py" ]
