#ensure libpython up to date
sudo apt-get install libpython-dev

#install mysql, see README for config instructions
sudo apt-get install libmysqlclient-dev
sudo apt-get install mysql-server --fix-missing
sudo apt-get install mysql-client

#install mysql-connector-python
cd ~
git clone https://github.com/mysql/mysql-connector-python.git
cd mysql-connector-python
python ./setup.py build
sudo python ./setup.py install

#install pip packages
cd ~/mqttProxReader/install_scripts
sudo pip install -r requirements.txt

sudo npm install -g python-shell
