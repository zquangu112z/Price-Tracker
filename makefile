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


