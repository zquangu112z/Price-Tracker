## Tracking Price App
- Status: developing

## Setup project
### Install dependencies
```bash
make setup-dependencies
```
### Init database
```bash
make initdb
```

## Deploy 
```bash
export MAIL_USERNAME=<MAIL_USERNAME>
export MAIL_PASSWORD=<MAIL_PASSWORD>
modd
```


## Run scheduler
### Terminal 1
```bash
PYTHONPATH=src celery -A pricetracker.celery worker
```
### Terminal 2
```bash
PYTHONPATH=src celery -A pricetracker.celery beat
```