#!/bin/bash
echo ""
#service nginx status
#systemctl status gunicorn.service
#echo ""
#service arp_block status
#echo "   arp_block processes:"
#ps aux | grep arp_block| grep python
echo ""
service dnsmasq status
service hostapd status


