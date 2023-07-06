FROM continuumio/anaconda3

WORKDIR /usr/src/systems-integrated-development

RUN apt-get update
RUN apt install -y gfortran libblas-dev liblapack-dev
RUN conda install -y numpy scipy

ENTRYPOINT [ "/bin/bash" ]
