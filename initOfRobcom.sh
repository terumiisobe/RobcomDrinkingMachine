\#!/bin/bash
#Author: Lucas C. Tavano
#Date: 06/01/2018
echo ""
echo "--iniciando Robson--"

if [ 1 ]
    then
        echo "-->Iniciando antena interna..."
        MAC_WLAN="wlan0"
        service networking restart
        rfkill unblock wlan
        ifconfig wlan0 down
        sleep 1
        ifconfig wlan0 up
        echo "-->Conectando na internet..."
        service wpa_supplicant stop
        sleep 1
        wpa_supplicant -Dnl80211 -iwlan0 -c/home/pi/RobcomDrinkingMachine/wpa.conf -B
        sleep 1
        dhclient wlan0
        #iwconfig wlan0 essid Batwifi key s:segundaocaralho
        #Configuração em /etc/network/interfaces
        #sleep 1
        #dhclient wlan0
        echo "-->Iniciando antena externa..."
        ifconfig wlan1 down
        sleep 1
        ifconfig wlan1 192.168.241.1/24 up

        killall hostapd
        killall dnsmasq
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
        /home/pi/RobcomDrinkingMachine/bluetooth_connect.sh &
        sleep 3
        #/home/pi/RobcomDrinkingMachine/RobcomWebService/RobcomWebService.py &
        echo ""
        echo " ---> Robson is Alive!!!"
        #Guarda data de quando esse programa rodou
        #echo 0 > /root/info/lock
        #echo 0 > /root/info/forced_unlock
    else
        exit 0
fi
