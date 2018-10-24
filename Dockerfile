FROM ubuntu:18.04
ADD . /src
WORKDIR src/
ENV PORT $PORT
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
RUN chmod 777 start.sh
CMD ["./start.sh"]
