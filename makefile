deploy:
	pip install --editable . && export FLASK_APP=pricetracker && flask run

deploy2:
	export FLASK_APP=pricetracker && export PYTHONPATH=./src && flask run

