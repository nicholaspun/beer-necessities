FROM python:3-stretch

RUN pip install nltk

# TODO: Slim this down?
RUN python -m nltk.downloader -d /usr/local/share/nltk_data all

ADD senna-v3.0.tgz /senna

COPY scripts/ /scripts

WORKDIR /scripts

CMD [ "python", "csv_to_obj.py" ]
