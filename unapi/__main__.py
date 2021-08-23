# -*- coding: utf-8 -*-

import argparse
from lxml import etree

from .log import logger
from .client import Client
from .utils import pretty_json, pretty_xml


def main():
    unapi_cli = argparse.ArgumentParser("unapi", description='')
    unapi_cli.add_argument('--url', type=str, help='URL of unAPI endpoint', default="https://unapi.k10plus.de")
    unapi_cli.add_argument('--db', type=str, help='name of target DB', default="swb")
    unapi_cli.add_argument('--var', type=str, help='type of identifier', default="ppn")
    unapi_cli.add_argument('--record', type=str, help='identifier of record')
    unapi_cli.add_argument('--schema', type=str, help='schema of record', default="picajson")
    unapi_cli.add_argument('--formats', type=bool, help='show supported formats', nargs="?", const=True, default=False)
    unapi_args = unapi_cli.parse_args()
    client = Client(unapi_args.url, unapi_args.db, unapi_args.var)
    if unapi_args.formats:
        supported = client.formats.keys()
        logger.info("Database '{0}' supports the following formats:\n- {1}".format(client.DB, "\n- ".join(supported)))
        return
    if unapi_args.record is None:
        unapi_cli.print_help()
        return
    response = client.request(unapi_args.record, unapi_args.schema)
    if type(response) == dict or type(response) == list:
        response = pretty_json(response)
    if type(response) == etree._Element:
        response = pretty_xml(response)
    if response is not None:
        print(response)
        return


if __name__ == '__main__':
    main()
