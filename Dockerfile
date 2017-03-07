FROM python:3.6
ADD . /whitespace
WORKDIR /whitespace
RUN pip install -r requirements.txt
