# This shell scripts requires Python 3.9+ and Node with NPM installed

# install python requirements
pip install -r requirements.txt

# install ionic 6
npm install -g @angular/cli
npm install -g @ionic/cli@6

# start python backend
mkdir logs
nohup python ./src/api/run.py > logs/api.log.txt 2>&1 &
