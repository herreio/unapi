# -*- coding: utf-8 -*-

import argparse

from .client import Client
from .utils import pretty_json, pretty_xml


def main():
    unapi_cli = argparse.ArgumentParser("unapi", description='')
    unapi_cli.add_argument('--url', type=str, help='URL of unAPI endpoint', default="https://unapi.k10plus.de")
    unapi_cli.add_argument('--db', type=str, help='name of target DB', default="swb")
    unapi_cli.add_argument('--var', type=str, help='type of identifier', default="ppn")
    unapi_cli.add_argument('--record', type=str, help='identifier of record')
    unapi_cli.add_argument('--schema', type=str, help='schema of record', default="picajson")
    unapi_args = unapi_cli.parse_args()
    if not unapi_args.record:
        unapi_cli.print_help()
        return
    client = Client(unapi_args.url, unapi_args.db, unapi_args.var)
    response = client.request(unapi_args.record, unapi_args.schema)
    if "json" in unapi_args.schema:
        response = pretty_json(response)
    if "xml" in unapi_args.schema:
        response = pretty_xml(response)
    if response is not None:
        print(response)
        return


if __name__ == '__main__':
    main()
