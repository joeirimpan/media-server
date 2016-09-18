# -*- coding: utf-8 -*-
import nmap

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Document
from forms import DocumentForm


import os
module_dir = os.path.dirname(__file__)  # get current directory
exec_file_path = os.path.join(module_dir, 'Shared_Folder/start_server.py')

import socket
server_addr=socket.gethostbyname(socket.gethostname())
import nmap
import subprocess

from helpers import get_lan_ip

#show the devices in local network

def scan_list(request):
    hosts= str(get_lan_ip()) + "/24"
    nmap_args = "-sP"
    scanner = nmap.PortScanner()
    scanner.scan(hosts=hosts, arguments=nmap_args)
    hostList = []
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')

    for ip in scanner.all_hosts():
        print 'Host : %s (%s)' % (ip, scanner[ip].hostname())
        host = {"ip" : ip}
        if "hostname" in scanner[ip]:
          host["hostname"] = scanner[ip]["hostname"]
        if "mac" in scanner[ip]["addresses"]:
          host["mac"] = scanner[ip]["addresses"]["mac"].upper()
        hostList.append(host)

    return render(
        request,
        'device_list.html',
        {'hostList': hostList, 'clientIp' : client_ip,'serverAddr' : server_addr}
    )
#start python simple http server
def start_server(request):
    subprocess.Popen(['.', exec_file_path], shell=True )
    return render(
        request,
        'start_server.html',
        {'serverAddr': server_addr + ':8005'}
    )


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )
  
