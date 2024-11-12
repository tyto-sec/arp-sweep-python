# ARP Sweep Script

This Python script performs an ARP sweep to identify active hosts on a specified network. The script allows customization of delays between requests, timeout durations, and options for using random source IPs or sending gratuitous ARP packets.

## Features

- **ARP Request Sweep**: Sends ARP requests to hosts on the specified network to check if they are active.
- **Randomized Source IP**: Optionally sends ARP requests with a random source IP within the network.
- **Gratuitous ARP**: Periodically sends gratuitous ARP packets for the host's own IP to update ARP caches on the network.
- **Adjustable Delay and Timeout**: Configurable delay between packets and timeout for responses.
- **Verbose Output**: Optionally provides detailed output, showing whether each host is up or down.

## Prerequisites

- **Python 3**: The script requires Python 3.
- **Scapy**: Install with `pip install scapy`.
- **Network Permissions**: Running the script requires permissions to send ARP packets, typically root or administrator privileges.

## Usage

Run the script with the target network in CIDR notation and optional flags to configure the sweep.

```bash
sudo python3 arp_sweep.py <network> [-m <min_delay>] [-M <max_delay>] [-t <timeout>] [-r] [-g] [-v]
```

### Arguments

- **network**: (Required) Network address in CIDR notation (e.g., `192.168.0.0/24`).
- **-m, --min-delay**: Minimum delay between ARP requests in seconds (default 0.1).
- **-M, --max-delay**: Maximum delay between ARP requests in seconds (default 2.0).
- **-t, --timeout**: Timeout in seconds to wait for an ARP response (default 1.0).
- **-r, --random-ip**: Use a random source IP address from the network for each ARP request.
- **-g, --gratuitous-arp**: Periodically send gratuitous ARP packets to update the ARP cache on other devices.
- **-v, --verbose**: Activate verbose mode to display down hosts in addition to active hosts.

## Notes

- **Permissions**: ARP requests typically require root privileges, so you may need to run the script with `sudo`.
- **Network Load Management**: Use `-m` and `-M` to manage the sweep’s impact on the network by setting minimum and maximum delays.

## Author

Written by tyto.
