FROM python:3.6

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

ADD . /whitespace
WORKDIR /whitespace
RUN pip install -r requirements.txt
RUN pip install gunicorn

# run the app server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:app"]