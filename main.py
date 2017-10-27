
import datetime
import ipaddress

import jinja2
import requests

cidr_url = "http://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone"

networks = []
resp = requests.get(cidr_url)
for line in resp.content.splitlines():
    networks.append(ipaddress.IPv4Network(line.decode("utf-8")))

proxy_expr = "SOCKS5 localhost:1086"
with open("pac.j2") as f:
    pac = jinja2.Template(f.read()).render(networks=networks, date=datetime.datetime.now(
        datetime.timezone.utc), proxy_expr=proxy_expr)
    print(pac)
