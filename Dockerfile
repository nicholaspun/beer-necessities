FROM python:3-stretch

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# TODO: Slim this down?
# RUN python -m nltk.downloader -d /usr/local/share/nltk_data all
#
# ADD senna-v3.0.tgz /senna

WORKDIR /beer-necessities

COPY module/ /beer-necessities/module
# COPY scripts/ /beer-necessities/scripts
COPY app.py /beer-necessities/app.py

RUN export FLASK_APP=app.py
CMD [ "flask", "run" ]
