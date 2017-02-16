# Indoor wifi positioning

### Hardware
Raspberry pi 3 running on Raspbian 8.0 (jessie) OS


### Installation
1. run 'git clone https://github.com/fe1t/Indoor-wifi-positioning'
2. then 'sudo sh installation_things.sh'


### Usage
1. You need to run 'sudo python documents/wifi_positioning_rssi_normal_dist_based/main.py' to collect data.
2. Position (x, y) you can find by using maps/z2f.html
3. run 'sudo python ./calculation_numpy.py' to determine your current position

> NOTE: There will be an accuracy problem: ~ 1-3 m *


### References
1. http://coursesweb.net/javascript/get-mouse-coordinates-inside-div-image_s2
2. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.527.2170&rep=rep1&type=pdf
3. http://www.mdpi.com/1424-8220/15/9/21824/htm 
