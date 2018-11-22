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
        ifconfig $MAC_WLAN down
        sleep 1
        ifconfig $MAC_WLAN 192.168.241.1/24 up

        killall hostapd
        killall dnsmasq

        echo "->Iniciando sistemas principais..."
        #echo "ok."
        echo "-->Iniciando dnsmasq..."
        sleep 1
        service dnsmasq start
        while [ $? == 1 ]; do #1 == FAIL
            echo "Reiniciando dnsmasq..."
            service dnsmasq stop
            sleep 1
            service dnsmasq start
        done
        echo "ok."
        echo "-->Unbloking wifi e wlan..."
        rfkill unblock wifi
        rfkill unblock wlan
        echo "-->Iniciando Firewall..."
        /home/pi/RobcomDrinkingMachine/firewall.sh
        sleep 2
        echo "-->Iniciando hostapd..."
        ifconfig wlan1 down
        service hostapd stop  #As vezes host apd nao liga por conta do unblock wifi
        sleep 8
        service hostapd start
        sleep 1
	echo "-->Iniciando nginx..."
        service nginx stop
        sleep 3
        service nginx start
        sleep 3
	echo "-->Iniciando gunicorn..."
        service gunicorn stop
        sleep 3
        service gunicorn start
	echo "-->Iniciando bluetooth..."
        service bluetooth stop
        sleep 3
        service bluetooth start
        sleep 1
        hciconfig hci0 up
        sleep 2
        for i in $(pgrep rfcomm); do kill $i; done;
        for i in $(pgrep bluetooth_conn); do kill $i; done;
        sleep 1
        ./bluetooth_connect.sh &
        sleep 3
        echo ""
        echo " ---> Robson is Alive!!!"
        #Guarda data de quando esse programa rodou
        #echo 0 > /root/info/lock
        #echo 0 > /root/info/forced_unlock
    else
        exit 0
fi
