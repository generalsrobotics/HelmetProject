sudo ifconfig ra0 192.168.42.1
sudo mv /etc/dhcp/dhcp.conf /etc/dhcp/dhcp.conf.bak
sudo cp ./dhcp.conf /etc/dhcp/dhcp.conf
sudo cp ./isc-dhcp-server /etc/default/isc-dhcp-server
sudo service isc-dhcp-server restart
