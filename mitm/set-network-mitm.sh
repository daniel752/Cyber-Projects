#!/bin/bash

table=""
chain_rule=""
protocol=""
dest_port=""
target=""
to_port=""

# Function to display script usage
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "-t: Name of the table"
    echo "-c: Chain rule"
    echo "-p: Protocol"
    echo "-d: Destination port"
    echo "-a: Target"
    echo "-o: Port to redirect to"
    echo "-h, --help: Display usage information"
}

# Parse command line options with getopts
while getopts "t:c:p:d:a:o:h" opt; do
    case $opt in
        t)  table="$OPTARG" ;;
        c)  chain_rule="$OPTARG" ;;
        p)  protocol="$OPTARG" ;;
        d)  dest_port="$OPTARG" ;;
        a)  target="$OPTARG" ;;
        o)  to_port="$OPTARG" ;;
        h)  usage; exit 0 ;;
        \?) echo "Invalid option -$OPTARG" >&2; usage; exit 1 ;;
    esac
done

echo "Table: $table"
echo "Chain rule: $chain_rule"
echo "Protocol: $protocol"
echo "Redirect to port: $dest_port"
echo "Target: $target"
echo "Listen to port: $to_port"

# IP forwarding, enables interfaces on the system to forward packets to one other.
echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -t "$table" -A "$chain_rule" -p "$protocol" --destination-port "$dest_port" -j "$target" --to-port "$to_port"

iptables -I INPUT 1 -p tcp --dport 8080 -j ACCEPT

echo "\nNetwork is ready for MITM"
echo "Leave this terminal open so iptables settings will still apply. When you close the terminal, iptables settings will revert back to default"

ctrl_c() {
    echo "\nStopped redirecting $dest_port to $to_port by user"
    iptables -t "$table" -D "$chain_rule" -p "$protocol" --destination-port "$dest_port" -j "$target" --to-port "$to_port"
    iptables -D INPUT 1
    echo "Reverted settings added to iptables"
    exit 0
}

trap ctrl_c INT

while true; do
    sleep 1
done

