# -*- coding: utf-8 -*-

import logging
from . import utils


class Client:
    """
    unAPI client for DB identified by key at given URL with specified identifier type.
    """

    def __init__(self, url="https://unapi.k10plus.de", key="opac-de-627", idtype="ppn", loglevel=logging.DEBUG):
        self.url = url
        self.key = key
        self.idtype = idtype
        self.logger = utils.get_logger(loglevel)

    @property
    def formats(self):
        """
        Get a dictionary with supported data formats.
        """
        response = utils.get_request(self.url)
        response = utils.response_xml(response)
        if response is not None:
            schemas = [c for c in response.getchildren()]
            formats = {}
            for s in schemas:
                n = s.attrib['name']
                formats[n] = {}
                if 'type' in s.attrib:
                    formats[n]['type'] = s.attrib['type']
                else:
                    formats[n]['type'] = None
                if 'docs' in s.attrib:
                    formats[n]['docs'] = s.attrib['docs']
                else:
                    formats[n]['docs'] = None
            return formats

    def address(self, idvalue, format):
        """
        Get URL of record specified by ID value in given format.
        """
        return self.url + "/?id=" + self.key + ":" + \
            self.idtype + ":" + idvalue + "&format=" + format

    def request(self, idvalue, format, plain=False, lazy=False):
        """
        Request data of record specified by ID value in given format.
        """
        if not lazy:
            formats = self.formats
            if formats is None:
                return None
            if format not in formats:
                self.logger.error("Format '{0}' is unsupported!".format(format))
                return None
            formattype = formats[format]['type']
        self.logger.info("Request record {0} in format '{1}' from DB '{2}'.".format(idvalue, format, self.key))
        url = self.address(idvalue, format)
        response = utils.get_request(url)
        if response is not None:
            if plain or lazy:
                return utils.response_text(response)
            else:
                if "xml" in formattype:
                    return utils.response_xml(response)
                elif "json" in formattype:
                    return utils.response_json(response)
                else:
                    return utils.response_text(response)
