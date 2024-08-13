
###################################################################
# Builder image

#FROM ubuntu:22.04 as Builder
FROM ubuntu:24.04 as Builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    build-essential  \
    python3-dev python3-pip python3-setuptools python3-venv \
    cmake wget && \
    rm -rf /var/lib/apt/lists/  


# Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD requirements.txt /
RUN python3 -m pip install --upgrade pip && \
	python3 -m pip install -r requirements.txt

# Build ObsLn
ADD . /src/obsln
RUN cd /src/obsln && \
	python3 ./setup.py install


###################################################################
# Run time

#FROM ubuntu:22.04 
FROM ubuntu:24.04

RUN apt-get update && \
	apt-get install -y --no-install-recommends  \
	python3 python3-venv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#COPY --from=Builder /usr/lib/python3 /usr/lib/python3

COPY --from=Builder /opt/venv/lib/python3.12 /opt/venv/lib/python3.12/	



#ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.12/dist-packages/"
#ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.12/site-packages/"
#ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/usr/local/lib/:/usr/local/lib/python3.10/dist-packages/:/usr/local/lib/python3.10/site-packages/"


#ENTRYPOINT ["/bin/bash"]
##CMD ["-c","echo hello-world"]
