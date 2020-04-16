FROM tensorflow/tensorflow:1.14.0-py3

ADD ./*.* /
RUN pip3 install -r requirements.txt

RUN mkdir /models/ && \
    gdown --id 1arugGgNGequ5QxklqDDhsP6OSAlDNU5c -O models/355M-phil-v3.tar && \
    tar -C models/ -xcf models/355M-phil-v3.tar && \
    mv models/checkpoint/355M-phil-v3/ models && \
    rm models/355M-phil-v3.tar

RUN mkdir /src
ADD ./src/* /src/

# RUN mkdir -p /models/355M-phil-v3
# ADD ./models/355M-phil-v3 /models/355M-phil-v3

CMD python3 src/server.py $PORT $MODEL
