FROM tensorflow/tensorflow:1.14.0-py3

ADD ./*.* /
RUN pip3 install -r requirements.txt
RUN python3 download_model.py 124M

RUN mkdir /src
ADD ./src/* /src/

CMD python3 src/server.py $PORT
