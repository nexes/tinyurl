FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD . /code
RUN echo "docker file run" &&\
    pip install -r requirements.txt &&\
    ./django-migrations.sh

CMD python3 manage.py runserver 0.0.0.0:$PORT
