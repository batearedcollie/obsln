
ObsLn
======

Introduction
------------

Provides some of the basic functionality from ObsPy without many of the dependencies and size. For full ObsPy functionality please see the ObsPy project on GitHub [here](https://github.com/obspy)


Building Docker Image
---------------------

	docker build -t obsln:latest .


Running Examples in Docker Image
--------------------------------


	docker run --entrypoint=/usr/bin/python3 obsln:latest -c "runtest.py"