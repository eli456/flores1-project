FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /flores/
WORKDIR /flores
COPY requirements.txt /flores/
RUN pip install -r requirements.txt
COPY . /flores/
CMD sudo python manage.py runserver --settings=settings.production 0.0.0.0:8080