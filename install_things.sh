apt -y update
echo "mysql-server-5.5 mysql-server/root_password password toor" | debconf-set-selections
echo "mysql-server-5.5 mysql-server/root_password_again password toor" | debconf-set-selections
apt-get -y install mysql-server-5.5

curl -kO https://bootstrap.pypa.io/get-pip.py
python get-pip.py
apt -y install python-dev libmysqlclient-dev
pip install -r requirements.txt
mysql -uroot -ptoor -e "CREATE DATABASE IF NOT EXISTS collecting_ap; 
DROP TABLE IF EXISTS `access_point`;
 /*!40101 SET @saved_cs_client     = @@character_set_client */;
 /*!40101 SET character_set_client = utf8 */;
 CREATE TABLE `access_point` (
   `Id` int(11) NOT NULL AUTO_INCREMENT,
   `Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   `X` decimal(10,5) DEFAULT NULL,
   `Y` decimal(10,5) DEFAULT NULL,
   `ESSID` varchar(127) DEFAULT NULL,
   `BSSID` varchar(127) DEFAULT NULL,
   `RSSI` int(11) DEFAULT NULL,
   `quality_level` decimal(4,1) DEFAULT NULL,
   `quality_total` decimal(4,1) DEFAULT NULL,
   PRIMARY KEY (`Id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=22258 DEFAULT CHARSET=latin1;"

