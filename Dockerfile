# Motion Signal Technologies Ltd.
# All rights reserved
#
# The contents of this file are considered proprietary and usage or
# reproduction without prior authorization is strictly prohibited.

###################################################################
# Builder image

FROM ubuntu:18.04 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    build-essential  \
    python3-dev python3-pip python3-setuptools \
    cmake wget && \
    rm -rf /var/lib/apt/lists/  


#ADD container-src/requirements.txt /
#RUN python3 -m pip install --upgrade pip && \
#	python3 -m pip install -r requirements.txt


# Build ObsLn



###################################################################
# Run time







ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.6/dist-packages/"
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.6/site-packages/"
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/usr/local/lib/:/usr/local/lib/python3.6/dist-packages/:/usr/local/lib/python3.6/site-packages/"


ENTRYPOINT ["/bin/bash"]
#CMD ["-c","echo hello-world"]
