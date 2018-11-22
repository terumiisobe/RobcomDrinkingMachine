#!/bin/bash
for i in $(pgrep rfcomm); do kill $i; done;

while :; do
    rfcomm connect hci0 98:D3:33:80:8E:AE
    sleep 10
done
