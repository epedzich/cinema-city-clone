FROM python:3.6.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh \
    && chmod +x /start-celeryworker.sh

COPY ./celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh \
    && chmod +x /start-celerybeat.sh

COPY ./celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r//' /start-flower.sh \
    && chmod +x /start-flower.sh

COPY . /app

EXPOSE 8000

ENV \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH="/app:${PYTHONPATH}"

CMD ["python", "/app/manage.py", "runserver"]
