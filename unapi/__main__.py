# -*- coding: utf-8 -*-

import argparse
from lxml import etree

from .log import logger
from .client import Client
from .utils import pretty_json, pretty_xml


def main():
    unapi_cli = argparse.ArgumentParser("unapi", description='unAPI client for retrieving data from K10plus')
    unapi_cli.add_argument('--url', type=str, help='URL of unAPI endpoint', default="https://unapi.k10plus.de")
    unapi_cli.add_argument('--db', type=str, help='key of target DB', default="swb")
    unapi_cli.add_argument('--idtype', type=str, help='identifier type', default="ppn")
    unapi_cli.add_argument('--id', type=str, help='record identifier')
    unapi_cli.add_argument('--format', type=str, help='record format', default="picajson")
    unapi_cli.add_argument('--formats', type=bool, help='show supported formats', nargs="?", const=True, default=False)
    unapi_args = unapi_cli.parse_args()
    client = Client(url=unapi_args.url, key=unapi_args.db, idtype=unapi_args.idtype)
    if unapi_args.formats:
        supported = client.formats.keys()
        logger.info("Database '{0}' supports the following formats:\n- {1}".format(client.db, "\n- ".join(supported)))
        return
    if unapi_args.id is None:
        unapi_cli.print_help()
        return
    response = client.request(unapi_args.id, unapi_args.format)
    if type(response) == dict or type(response) == list:
        response = pretty_json(response)
    if type(response) == etree._Element:
        response = pretty_xml(response)
    if response is not None:
        print(response)
        return


if __name__ == '__main__':
    main()
