# deploy:
# 	pip install --editable . && export FLASK_APP=pricetracker && flask run

setup-dependencies:
	pip install -r requirements.txt
	npm install

initdb:
	export FLASK_APP=src/pricetracker/base.py && flask initdb


