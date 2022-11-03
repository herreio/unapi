# -*- coding: utf-8 -*-

import logging
import argparse

from .client import Client


def main():
    unapi_cli = argparse.ArgumentParser("unapi", description='unAPI client for retrieving data from K10plus')
    unapi_cli.add_argument('--url', type=str, help='URL of unAPI endpoint', default="https://unapi.k10plus.de")
    unapi_cli.add_argument('--db', type=str, help='key of target DB', default="opac-de-627")
    unapi_cli.add_argument('--idtype', type=str, help='identifier type', default="ppn")
    unapi_cli.add_argument('--id', type=str, help='record identifier')
    unapi_cli.add_argument('--format', type=str, help='record format', default="pp")
    unapi_cli.add_argument('--formats', type=bool, help='show supported formats', nargs="?", const=True, default=False)
    unapi_cli.add_argument('--debug', type=bool, help='set log level to debug', nargs="?", const=True, default=False)
    unapi_args = unapi_cli.parse_args()
    loglevel = logging.DEBUG if unapi_args.debug else logging.WARNING
    client = Client(
        url=unapi_args.url,
        key=unapi_args.db,
        idtype=unapi_args.idtype,
        loglevel=loglevel)
    if unapi_args.formats:
        supported = list(client.formats.keys())
        supported.sort()
        print("Database '{0}' supports the following formats:\n- {1}".format(client.key, "\n- ".join(supported)))
        return None
    if unapi_args.id is None:
        unapi_cli.print_help()
        return None
    response = client.request(unapi_args.id, unapi_args.format, plain=True)
    if response is not None:
        print(response)
        return None


if __name__ == '__main__':
    main()
