FROM python:3

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY src/ /src

#SHELL ["bash"]
ARG SRV_PORT=8881
EXPOSE $SRV_PORT
ENV SRV_PORT=$SRV_PORT

CMD python src/encryption_service.py -p $SRV_PORT