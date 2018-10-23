FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
COPY fairapp /src/fairapp
COPY projectsfair /src/projectsfair
COPY templates /src/templates
COPY manage.py /src
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate
CMD python3 manage.py runserver
