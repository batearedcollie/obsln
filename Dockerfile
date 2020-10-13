
###################################################################
# Builder image

FROM ubuntu:18.04 as Builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    build-essential  \
    python3-dev python3-pip python3-setuptools \
    cmake wget && \
    rm -rf /var/lib/apt/lists/  


ADD requirements.txt /
RUN python3 -m pip install --upgrade pip && \
	python3 -m pip install -r requirements.txt

# Build ObsLn
ADD . /src/obsln
RUN cd /src/obsln && \
	python3 ./setup.py install


###################################################################
# Run time

FROM ubuntu:18.04 

RUN apt-get update && \
	apt-get install -y --no-install-recommends  \
	python3

COPY --from=Builder /usr/lib/python3 /usr/lib/python3
COPY --from=Builder /usr/lib/python3.6 /usr/lib/python3.6	
COPY --from=Builder /usr/local/lib/python3.6 /usr/local/lib/python3.6 


ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.6/dist-packages/"
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.6/site-packages/"
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/usr/local/lib/:/usr/local/lib/python3.6/dist-packages/:/usr/local/lib/python3.6/site-packages/"


ENTRYPOINT ["/bin/bash"]
#CMD ["-c","echo hello-world"]
