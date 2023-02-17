FROM python:3.10

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade -r /app/requirements.txt

# TODO: Bind mount app-content to dynamicaly update website content
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./database /app/database
COPY ./app.py /app/

# TODO: Import env variables instead of copying .env file
COPY .env /app/
COPY client_secret.json /app/

CMD python app.py
