#!/bin/bash
for i in $(pgrep rfcomm); do kill $i; done;
while :; do
    #for i in $(pgrep bluetooth_conn); do kill $i; done;
    BT=`ls /dev/ | grep rfcomm`
    echo $BT
    if [ $BT!="rfcomm0" ];
    then
        rfcomm connect hci0 98:D3:33:80:8E:AE
    else
        echo "Conexao ok, diretorio /dev/rfcomm0 encontrado"
    fi
    sleep 10
done
