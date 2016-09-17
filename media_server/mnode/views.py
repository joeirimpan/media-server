from django.shortcuts import render

import nmap

from helpers import get_lan_ip


def scan_list(request):

    hosts= str(get_lan_ip()) + "/24"
    nmap_args = "-sn"
    scanner = nmap.PortScanner()
    scanner.scan(hosts=hosts, arguments=nmap_args)
    hostList = []

    for ip in scanner.all_hosts():
        host = {"ip" : ip}
        if "hostname" in scanner[ip]:
          host["hostname"] = scanner[ip]["hostname"]
        if "mac" in scanner[ip]["addresses"]:
          host["mac"] = scanner[ip]["addresses"]["mac"].upper()
        hostList.append(host)

    return render(
        request,
        'templates/device_list.html',
        {'hostList': hostList}
    )
