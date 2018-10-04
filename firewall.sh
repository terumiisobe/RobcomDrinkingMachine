#!/bin/bash
#########################################################################
#Author: Lucas Tavano <lc_tavano@hotmail.com>, Gustavo Lepri            #
#date: 22/02/2018                                                       #
#reviewed at: 26/06/2018                                                #
#########################################################################
# Interface de rede de output
IFACE_WEB="eth0"
# Interface de rede ligada a rede interna
IFACE_LAN="wlan0"
IFACE_IP="12.168.25.1"

function start() {
# Limpa todas as regras
iptables -F
iptables -t nat -F
iptables -t mangle -F
# Coloca as políticas padrões como ACCEPT, liberando todo e qualquer acesso
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
# Habilita o roteamento no kernel #
echo 1 > /proc/sys/net/ipv4/ip_forward
# Compartilha a internet
iptables -t nat -A POSTROUTING -o $IFACE_WEB -j MASQUERADE

#iptables -t nat -A PREROUTING -i $IFACE_LAN -p udp -m udp --dport 53 -j DNAT --to-destination 8.8.8.8
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p tcp -m tcp --dport 53 -j DNAT --to-destination 8.8.8.8
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p udp -m udp --dport 53 -j DNAT --to-destination 8.8.4.4
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p tcp -m tcp --dport 53 -j DNAT --to-destination 8.8.4.4


#iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -m mark ! --mark 0x63 -j DNAT --to-destination 192.168.25.1:80
#iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 443 -m mark ! --mark 0x63 -j DNAT --to-destination 192.168.25.1:443
iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -j DNAT --to-destination 192.168.25.1:80
iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 443 -j DNAT --to-destination 192.168.25.1:443

iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
}

start;
