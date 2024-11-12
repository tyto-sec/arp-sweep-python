#!/usr/bin/python3

from scapy.all import Ether, ARP, srp1, sendp, get_if_hwaddr, get_if_addr, conf
import random
import time
import argparse
import ipaddress


def random_sleep(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))


def generate_random_ip(network):
    return str(random.choice(list(network.hosts())))


def arp_request(target_ip, src_mac, src_ip, timeout, use_verbose):
    arp_pkt = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc=src_mac, psrc=src_ip, pdst=target_ip)
    response = srp1(arp_pkt, timeout=timeout, verbose=0)
    if response:
        print(f"[+] Host {target_ip} is up.")
    elif use_verbose:
        print(f"[-] Host {target_ip} is down.")

def gratuitous_arp(src_mac, src_ip):
    arp_pkt = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, hwsrc=src_mac, psrc=src_ip, pdst=src_ip)
    sendp(arp_pkt, verbose=0)


def arp_sweep(network, min_delay, max_delay, timeout, use_random_ip, use_gratuitous_arp, use_verbose):
    ips = [str(ip) for ip in network.hosts()]
    random.shuffle(ips)

    for target_ip in ips:
        src_mac = get_if_hwaddr(conf.iface)
        src_ip = generate_random_ip(network) if use_random_ip else get_if_addr(conf.iface)
        arp_request(target_ip, src_mac, src_ip, timeout, use_verbose)

        if use_gratuitous_arp and random.random() < 0.1:
            gratuitous_arp(src_mac, src_ip)

        random_sleep(min_delay, max_delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform an ARP sweep")
    parser.add_argument("network", help="Network to scan, e.g., 192.168.0.0/24")
    parser.add_argument("-m", "--min-delay", type=float, default=0, help="Minimum delay between packets (default 0.1s)")
    parser.add_argument("-M", "--max-delay", type=float, default=2.0, help="Maximum delay between packets (default 2.0s)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout for each ARP request (default 1.0s)")
    parser.add_argument("-r", "--random-ip", action="store_true", help="Use a random source IP")
    parser.add_argument("-g", "--gratuitous-arp", action="store_true", help="Send gratuitous ARP packets")
    parser.add_argument("-v", "--verbose", action="store_true", help="Activate verbose mode")

    args = parser.parse_args()

    try:
        network = ipaddress.ip_network(args.network)
    except ValueError:
        print("Invalid network. Use CIDR format, e.g., 192.168.0.0/24")
        exit(1)

    arp_sweep(network, args.min_delay, args.max_delay, args.timeout, args.random_ip, args.gratuitous_arp, args.verbose)
