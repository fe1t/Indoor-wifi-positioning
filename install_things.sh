apt -y update
echo "mysql-server-5.5 mysql-server/root_password password toor" | debconf-set-selections
echo "mysql-server-5.5 mysql-server/root_password_again password toor" | debconf-set-selections
apt -y install mysql-server-5.5

apt -y install rdate
rdate time1.google.com -vn

rm /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
rm /etc/timezone
echo "Asia/Tokyo" | sudo tee /etc/timezone

curl -kO https://bootstrap.pypa.io/get-pip.py
python get-pip.py
apt -y install python-dev libmysqlclient-dev
apt -y install libssl-dev
pip install -r requirements.txt
mysql -uroot -ptoor -e "CREATE DATABASE IF NOT EXISTS collecting_ap"
mysql -uroot -ptoor collecting_ap < wifi_database.sql
