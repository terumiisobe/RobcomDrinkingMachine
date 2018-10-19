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
IFACE_IP="192.168.241.1"

function start() {
# Limpa todas as regras
iptables -F
iptables -t nat -F
iptables -t mangle -F
# Coloca as políticas padrões como ACCEPT, liberando todo e qualquer acesso
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
# Carrega módulos #
/sbin/modprobe ip_tables
/sbin/modprobe iptable_filter
/sbin/modprobe ip_conntrack
/sbin/modprobe ip_conntrack_ftp
/sbin/modprobe nf_conntrack_ipv4
/sbin/modprobe ip_nat_ftp
/sbin/modprobe ipt_MASQUERADE
/sbin/modprobe iptable_mangle
/sbin/modprobe iptable_nat
/sbin/modprobe nf_nat
/sbin/modprobe nf_conntrack
/sbin/modprobe x_tables
/sbin/modprobe nf_nat_pptp

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp --dport 67 -j ACCEPT
iptables -A INPUT -p udp --dport 67 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p udp --dport 22 -j ACCEPT
#=================DNS=========================
iptables -A FORWARD -p tcp --dport 53 -j ACCEPT
iptables -A FORWARD -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
#=============================================
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p udp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p udp --dport 443 -j ACCEPT

# Habilita o roteamento no kernel #
echo 1 > /proc/sys/net/ipv4/ip_forward

#iptables -t nat -A PREROUTING -i $IFACE_LAN -p udp -m udp --dport 53 -j DNAT --to-destination 8.8.8.8
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p tcp -m tcp --dport 53 -j DNAT --to-destination 8.8.8.8
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p udp -m udp --dport 53 -j DNAT --to-destination 8.8.4.4
#iptables -t nat -A PREROUTING -i $IFACE_LAN -p tcp -m tcp --dport 53 -j DNAT --to-destination 8.8.4.4


#iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -m mark ! --mark 0x63 -j DNAT --to-destination 192.168.25.1:80
#iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 443 -m mark ! --mark 0x63 -j DNAT --to-destination 192.168.25.1:443
iptables -t nat -A PREROUTING -i wlan0 -j DNAT --to-destination 192.168.241.1:80
iptables -t nat -A PREROUTING -i wlan0 -j DNAT --to-destination 192.168.241.1:443
iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -j DNAT --to-destination 192.168.241.1:80
iptables -t nat -A PREROUTING -i wlan0 -p tcp -m tcp --dport 443 -j DNAT --to-destination 192.168.241.1:443

###########################################################
#Bloqueio dos sites e aplicativos para usuários deslogados#
###########################################################
#iptables -A FORWARD -m mark --mark 0x63 -j ACCEPT
#iptables -A FORWARD -m mark --mark 0x62 -j ACCEPT
iptables -A FORWARD -i $IFACE_LAN -j DROP

iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT

iptables -t nat -A POSTROUTING -o $IFACE_WEB -j MASQUERADE

}

start;
