FROM python:3.9

RUN pip install pylast ytmusicapi

COPY auth.json headers_auth.json main.py /

CMD [ "python", "-u", "./main.py" ]