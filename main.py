import datetime
import ipaddress
import os
from urllib import request

import jinja2
import click

cn_cidr_url = "http://www.ipdeny.com/ipblocks/data/aggregated/cn-aggregated.zone"

private_networks = [
    "10.0.0.0/8",
    "127.0.0.1/32",
    "100.64.0.0/10",
    "172.16.0.0/12",
    "192.168.0.0/16",
]


@click.command()
@click.option(
    "--proxy-expr", default="SOCKS5 localhost:1086", help="proxy expression")
def main(proxy_expr):
    networks = [ipaddress.IPv4Network(n) for n in private_networks]

    resp = request.urlopen(cn_cidr_url)
    for line in resp.readlines():
        cidr = line.decode("utf-8").strip()
        networks.append(ipaddress.IPv4Network(cidr))

    with open(os.path.join("template", "pac.j2")) as f:
        pac = jinja2.Template(f.read()).render(
            networks=networks,
            date=datetime.datetime.now(datetime.timezone.utc),
            proxy_expr=proxy_expr)
        print(pac)


if __name__ == '__main__':
    main()