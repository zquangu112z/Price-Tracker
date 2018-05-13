# deploy:
# 	pip install --editable . && export FLASK_APP=pricetracker && flask run

setup-dependencies:
	pip install -r requirements.txt
	sudo pip install -r requirements_global.txt
	npm install

initdb:
	export FLASK_APP=src/pricetracker/base.py && flask initdb


rsync:
	rsync -r ./ kilia@192.168.100.243:~/NicholasUbuntu/Price-Tracker/


# ---------- Run scheduled tasks ----------
# Terminal 1
make worker:
	PYTHONPATH=./src celery -A src.pricetracker.celery_worker worker 
# Terminal 1
make beat:
	PYTHONPATH=./src celery -A src.pricetracker.scheduler beat