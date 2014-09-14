echo "deb http://downloads.skewed.de/apt/saucy saucy universe" >> /etc/apt/sources.list
echo "deb-src http://downloads.skewed.de/apt/saucy saucy universe" >> /etc/apt/sources.list
#echo "deb https://ppa.launchpad.net/mapnik/boost/ubuntu saucy main" >> /etc/apt/sources.list
#echo "deb-src http://ppa.launchpad.net/mapnik/boos/ubuntu saucy main" >> /etc/apt/sources.list
apt-get update
apt-get install -y --force-yes python-graph-tool
