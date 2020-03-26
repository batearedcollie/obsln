
ObsLn
======

Introduction
------------

Provides some of the basic functionality from ObsPy without the bloated dependencies and size 

Building Docker Image
---------------------

..

	docker build -t obsln:latest .


Running Examples in Docker Image
--------------------------------

..

	docker run --entrypoint=/usr/bin/python3 obsln:latest -c "runtest.py"