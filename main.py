
import datetime
import ipaddress

import jinja2
import requests

cidr_url = "http://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone"

private_networks = ["10.0.0.0/8",
                    "127.0.0.1/32",
                    "100.64.0.0/10",
                    "172.16.0.0/12",
                    "192.168.0.0/16", ]
networks = [ipaddress.IPv4Network(n) for n in private_networks]
resp = requests.get(cidr_url)
for line in resp.content.splitlines():
    networks.append(ipaddress.IPv4Network(line.decode("utf-8")))

proxy_expr = "SOCKS5 localhost:1086"
with open("pac.j2") as f:
    pac = jinja2.Template(f.read()).render(networks=networks, date=datetime.datetime.now(
        datetime.timezone.utc), proxy_expr=proxy_expr)
    print(pac)
