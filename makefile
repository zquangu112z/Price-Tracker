# deploy:
# 	export FLASK_APP=pricetracker && export PYTHONPATH=./src && pip install --editable . && flask run

deploy2:
	export FLASK_APP=pricetracker && export PYTHONPATH=./src && flask run

deploy3:
	pip install --editable . && export FLASK_APP=pricetracker && flask run