FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    python-flask \
    python-pip \
    python-pandas \
    python-numpy \
    gnuplot-nox

RUN pip install gnuplotlib

ADD server.py /server.py

ENTRYPOINT ["python", "/server.py"]
