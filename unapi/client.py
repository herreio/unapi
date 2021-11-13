# -*- coding: utf-8 -*-

from . import utils
from .log import logger


class Client:
    """
    unAPI client for DB identified by key at given URL with specified identifier type.
    """

    def __init__(self, url="https://unapi.k10plus.de", key="opac-de-627", idtype="ppn"):
        self.url = url
        self.key = key
        self.idtype = idtype

    @property
    def formats(self):
        """
        Get a dictionary with supported data formats.
        """
        response = utils.get_request(self.url)
        response = utils.response_xml(response)
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

    def request(self, idvalue, format):
        """
        Request data of record specified by ID in given format.
        """
        logger.info("Request record {0} in format '{1}' from DB '{2}'.".format(idvalue, format, self.key))
        formats = self.formats
        if format in formats:
            formattype = formats[format]['type']
            url = self.address(idvalue, format)
            response = utils.get_request(url)
            if response is not None:
                if "xml" in formattype:
                    return utils.response_xml(response)
                elif "json" in formattype:
                    return utils.response_json(response)
                else:
                    return utils.response_text(response)
            else:
                return response
        else:
            logger.error("Format '{0}' is unsupported!".format(format))
            return None
