install:
	python -m pip install --upgrade pip &&\
	python -m pip install -r requirements.txt

lint:
	pylint --disable=R,C,W main.py

test:
	pytest

all: install lint test