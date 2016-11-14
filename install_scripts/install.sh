#ensure libpython up to date
sudo apt-get install libpython-dev

#install mysql, see README for config instructions
sudo apt-get install mysql-server --fix-missing
sudo apt-get install mysql-client

#install pip packages
sudo pip install -r requirements.txt

sudo npm install -g python-shell
