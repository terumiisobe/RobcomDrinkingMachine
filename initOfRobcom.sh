#!/bin/bash
#Author: Lucas C. Tavano
#Date: 06/01/2018
echo ""
echo "--iniciando Robson--"

if [ 1 ]
    then
        echo ""
        echo "--Iniciando initBash--"
        echo "Definindo interfaces de rede"
        #Pega MAC do adaptador
        MAC_WLAN="wlan0"

        service networking restart
        rfkill unblock wlan
        service network-manager restart
        ifconfig $MAC_WLAN down
        sleep 1
        ifconfig $MAC_WLAN 192.168.25.1/24 up

        killall hostapd
        killall dnsmasq

        echo "Iniciando sistemas principais..."
        #echo "ok."
        echo "Iniciando dnsmasq..."
        sleep 1
        service dnsmasq start
        while [ $? == 1 ]; do #1 == FAIL
            echo "Reiniciando dnsmasq..."
            service dnsmasq stop
            sleep 1
            service dnsmasq start
        done
        echo "ok."
        echo "Unbloking wifi e wlan..."
        rfkill unblock wifi
        rfkill unblock wlan
        echo "Iniciando Firewall..."
        /home/pi/RobcomDrinkingMachine/firewall.sh
        sleep 2
        echo "Iniciando hostapd..."
        service hostapd stop  #As vezes host apd nao liga por conta do unblock wifi
        service wpa_supplicant stop
        sleep 3
        service hostapd start
        sleep 1
        #service gunicorn stop
        sleep 3
        #service gunicorn start
        sleep 1
        echo ""
        echo "Robson is Alive!!!"
        #Guarda data de quando esse programa rodou
        #echo 0 > /root/info/lock
        #echo 0 > /root/info/forced_unlock
    else
        exit 0
fi
