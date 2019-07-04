FROM python:3.6.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

EXPOSE 8000

ENV \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH="/app:${PYTHONPATH}"

CMD ["python", "/app/manage.py", "runserver"]
