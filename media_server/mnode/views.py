from django.shortcuts import render
from django.http import HttpResponse

import nmap

from helpers import get_lan_ip

def scan_list(request):

    hosts= str(get_lan_ip()) + "/24"
    nmap_args = "-sn"
    scanner = nmap.PortScanner()
    scanner.scan(hosts=hosts, arguments=nmap_args)
    hostList = []
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')

    for ip in scanner.all_hosts():
        host = {"ip" : ip}
        if "hostname" in scanner[ip]:
          host["hostname"] = scanner[ip]["hostname"]
        if "mac" in scanner[ip]["addresses"]:
          host["mac"] = scanner[ip]["addresses"]["mac"].upper()
        hostList.append(host)
    return render(
        request,
        'device_list.html',
        {'hostList': hostList, 'clientIp' : client_ip}
    )
