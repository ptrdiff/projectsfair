FROM alpine:3.5
RUN apk add --update python py-pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY fairapp /src/fairapp
COPY projectsfair /src/projectsfair
COPY templates /src/templates
COPY manage.py /src
CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver
