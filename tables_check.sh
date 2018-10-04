#!/bin/bash
echo "--------------------------TABELA FILTER-----------------------------"
iptables -L -v -t filter

echo "--------------------------TABELA NAT--------------------------------"
iptables -L -v -t nat

echo "--------------------------TABELA MANGLE-----------------------------"
iptables -L -v -t mangle

