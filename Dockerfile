FROM python:3.6

RUN apt-get install -y libpq-dev

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY . /usr/src/app/

RUN pip install pipenv
RUN pipenv install && pipenv install --system

# CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]