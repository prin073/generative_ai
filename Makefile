setup:
	python3 -m venv venv

source:
	source venv/bin/activate #doesn't work with make

install_hackathon:
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install boto3 botocore awscli requests flask

install:
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements.txt

freeze:
	venv/bin/pip3 freeze > requirements.txt

