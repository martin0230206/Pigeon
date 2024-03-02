# Pigeon

### Project setup
#### Environment
```
cd /www/sender
python -m venv .venv
python -m pip install --upgrade pip
pip install -r requirements txt
```
#### Fastapi
```
cd /www/sender
source .venv/bin/activate
uvicorn main:app --port 24048
```
#### RQ-Dashboard
```
cd /www/sender
source .venv/bin/activate
rq-dashboard
```
#### rq worker
```
cd /www/sender
source .venv/bin/activate
rq worker sender -c main
```
