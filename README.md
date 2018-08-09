# LinuxGaming

This is my own Linux gaming aggregate webapp I built for personal use.

## Development

### Environment

Create a virtual environment in python3

```bash
python3 -m virtualenv venv
```

Load the environment

```bash
source ./venv/bin/activate
```

Install the requirements

```bash
pip install -r requirements.txt
```

Run the application in debug mode

```bash
FLASK_APP=run.py FLASK_DEBUG=1 python -m flask run
```


### Data import

If you are using MongoDB directly installed on your local machine or else where then skip the docker commands and go straight for the the import command.

Pull the latest MongoDB docker image.

```bash
docker pull mongo
```
Run the docker image in a throw away container.

```bash
docker run -p 27017:27017 -ti --rm mongo
```
Seed the data using mongo-import tool.

```bash
mongoimport --db linuxgamingthings --collection items --drop --file ./config/test_data.json
```


## Tooling

  - Python 3.6
  - Flask
  - MongoDB
  - AWS EBS
  - Gitlab CI
  - SemanticUI
