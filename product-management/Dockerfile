FROM python:3

ENV PYTHONBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . /code/

WORKDIR /code/api

ENTRYPOINT ["python"]

CMD ["app.py"]