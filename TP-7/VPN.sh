#!/bin/bash

dnf install wireguard-tools -y

hostname=`cat /etc/hostname`


wg genkey | tee /etc/wireguard/$hostname.key

cat /etc/wireguard/$hostname.key | wg pubkey | tee /etc/wireguard/$hostname.pub

private=`cat /etc/wireguard/$hostname.key`
public=`cat /etc/wireguard/$hostname.pub`

systemctl start systemd-resolved
systemctl enable systemd-resolved


echo "
[main]
dns=systemd-resolved

[logging]" | tee /etc/NetworkManager/NetworkManager.conf 


rm -f /etc/resolv.conf
ln -s /usr/lib/systemd/resolv.conf /etc/resolv.conf

systemctl restart NetworkManager

echo "[Interface]
Address = $1/24

PrivateKey = $private

PostUp = resolvectl dns %i 1.1.1.1 9.9.9.9; resolvectl domain %i ~.
PreDown = resolvectl revert %i

[Peer]
PublicKey = HwH8YqS0Cw0CSfKPMlAVatF1Oy8qlmuSFQjNRVePZGU=

AllowedIPs = 0.0.0.0/0

Endpoint = 10.7.1.100:51820

PersistentKeepalive = 25" | tee /etc/wireguard/$hostname.conf

echo "Please run the first command on the server before running the second command on here:"
echo "echo '[Peer]
PublicKey = $public

AllowedIPs = $1/24' | sudo tee -a /etc/wireguard/wg0.conf && sudo systemctl restart wg-quick@wg0.service"

echo "sudo wg-quick up $hostname"







