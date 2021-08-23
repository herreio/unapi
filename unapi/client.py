# -*- coding: utf-8 -*-

from . import utils
from .log import logger


class Client:
    """
    unAPI client for DB at given URL with entity identifiers of type VAR.
    """

    def __init__(self, URL="https://unapi.k10plus.de", DB="swb", VAR="ppn"):
        self.URL = URL
        self.DB = DB
        self.VAR = VAR

    @property
    def formats(self):
        """
        Get a dictionary with supported data formats.
        """
        response = utils.get_request(self.URL)
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

    def address(self, idn, schema):
        """
        Get URL of entity specified by IDN in given schema.
        """
        return self.URL + "/?id=" + self.DB + ":" + \
            self.VAR + ":" + idn + "&format=" + schema

    def request(self, idn, schema):
        """
        Request data of entity specified by IDN in given schema.
        """
        logger.info("Request record {0} in schema '{1}' from DB '{2}'.".format(idn, schema, self.DB))
        formats = self.formats
        if schema in formats:
            schematype = formats[schema]['type']
            url = self.address(idn, schema)
            response = utils.get_request(url)
            if response is not None:
                if "xml" in schematype:
                    return utils.response_xml(response)
                elif "json" in schematype:
                    return utils.response_json(response)
                else:
                    return utils.response_text(response)
            else:
                return response
        else:
            logger.error("Schema '{0}' is unsupported!".format(schema))
            return None
