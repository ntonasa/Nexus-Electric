# Makefile as a build automation tool for 
# automating various tasks in the repository

SHELL := /bin/bash
APT=apt-get install -y
PYTHON=python3
MANAGE=$(PYTHON) manage.py
PIP=pip3

help:
	@echo "Usage"

py_deps: requirements.txt
	$(PIP) install -r requirements.txt
