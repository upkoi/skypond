#!/usr/bin/env sh

# (thanks to André König for this method)
# https://dev.to/andre/docker-restricting-in--and-outbound-network-traffic-67p

ACCEPT_CIDR=${ALLOWED_CIDR:-192.168.0.0/16}

iptables -A INPUT -s $ACCEPT_CIDR -j ACCEPT
iptables -A INPUT -j DROP
iptables -A OUTPUT -d $ACCEPT_CIDR -j ACCEPT
iptables -A OUTPUT -j DROP

sudo -u app sh -c "$@"
