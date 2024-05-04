#!/usr/bin/python3

import sys
import os
import socket
import re
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth

def make_netloc(hostname, port):
    if port is None:
        return hostname
    else:
        return f'{hostname}:{port}'

def resolve_ip(url):
    p = urllib.parse.urlparse(url)
    print(f'Resolving IP of {p.hostname}...', end='')
    ip = socket.gethostbyname(p.hostname)
    print(ip)
    #
    if p.netloc == 'home.antocuni.eu:43780':
        netloc = make_netloc(ip, p.port)
        netloc = f'antocuni:sky@{netloc}'
    else:
        netloc = make_netloc(ip, p.port)

    p = p._replace(netloc=netloc)
    return urllib.parse.urlunparse(p)

def get_URLs():
    ROOT = 'http://home.antocuni.eu:43780/'
    auth = HTTPBasicAuth('antocuni', 'sky')
    r = re.compile('(?<=href=").*?(?=")')
    resp = requests.get(ROOT, auth=auth)
    flvs = [href for href in r.findall(resp.text) if href.endswith('.flv')]
    for i, href in enumerate(flvs):
        print(f'[{i:2}] {href}')
    print()
    x = input('Choose file(s) to download: ')
    idxs = map(int, x.split(','))
    urls = []
    for i in idxs:
        href = flvs[i]
        url = f'{ROOT}{href}'
        urls.append(url)
    print('\n'.join(urls))
    print()
    return urls

def main():
    if len(sys.argv) >= 2:
        URLs = sys.argv[1:]
    else:
        URLs = get_URLs()
    #
    URLs = [resolve_ip(url) for url in URLs]
    wget = '/data/local/tmp/busybox-armv7l wget'
    for url in URLs:
        print(url)
        cmd = f"""
        adb shell 'cd /sdcard/sky && {wget} -c "{url}"'
        """
        print()
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    main()
