import subprocess
import os
import sys
import nw_util
import time


def setup(essid, key, channel, interface, ip):
    try:
        subprocess.check_output("service network-manager stop", shell=True)
    except subprocess.CalledProcessError:
        print("Error stopping NW manager, might already be down", file=sys.stderr)
    # if we skip this sleep the network goes back to managed state,
    # probably because the network manager takes time to stop.
    # Experiments showed that making the network ad hoc and _then_ turning off
    # network manager would cause the device to be reset to the "Managed" mode.
    # Hence we assume that stopping the network manager resets the device, and we
    # sleep until that happens
    time.sleep(2)
    subprocess.check_output("ifconfig %s down" % interface, shell=True)
    subprocess.check_output("iwconfig %s mode ad-hoc" % interface, shell=True)
    subprocess.check_output("iwconfig %s channel %s" % (interface, channel), shell=True)
    subprocess.check_output("iwconfig %s essid %s" % (interface, essid), shell=True)
    subprocess.check_output("iwconfig %s key %s" % (interface, key), shell=True)
    subprocess.check_output("ifconfig %s %s" % (interface, ip), shell=True)


def main():
    if os.getuid() != 0:
        print("You need to be root to run this script! Exiting.")
        return

    if len(sys.argv) != 3:
        print("Invalid arguments.\nUsage: command essid key")
        return

    essid = sys.argv[1]
    key = sys.argv[2]

    ifs = nw_util.get_wireless_interfaces()

    if len(ifs) == 0:
        print("Looks like you don't have any wireless interfaces :( Stopping")
        return
    elif len(ifs) > 1:
        print("Detected wireless interfaces:", ifs)
        ip_if = input("Which wireless interface would you like to use?\n")
        if ip_if in ifs:
            chosen_if = ip_if
        else:
            "Invalid wireless interface entered, exiting"
            return
    else:
        chosen_if = ifs[0]

    print("Using interface:", chosen_if, file=sys.stderr)

    chosen_ip = nw_util.get_pseudo_unique_ip(chosen_if) + "/8"
    print("Using ip:", chosen_ip, file=sys.stderr)

    setup(essid, key, "1", chosen_if, chosen_ip)


main()
