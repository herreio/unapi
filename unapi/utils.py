# -*- coding: utf-8 -*-

import json
import requests
from lxml import etree
from .log import logger


def get_request(url, headers={}):
    """
    Send HTTP GET request to given URL.
    """
    if "User-Agent" not in headers:
        headers["User-Agent"] = "py-unapi 0.4.0"
    try:
        return requests.get(url, headers=headers)
    except requests.exceptions.RequestException as err:
        logger.error(err.__class__.__name__)
        return None


def response_ok(response):
    """
    Check if HTTP response is OK.
    """
    if response is None:
        return False
    if response.status_code == 200:
        return True
    else:
        logger.error("HTTP request to {0} failed!".format(response.url))
        logger.error("HTTP response code is {0}.".format(response.status_code))
        return False


def response_text(response):
    """
    Get text data from HTTP repsonse.
    """
    if response_ok(response):
        return response.text
    return ""


def response_json(response):
    """
    Get JSON data from HTTP repsonse.
    """
    if response_ok(response):
        if response.json() is not None:
            return response.json()
    return {}


def response_xml(response):
    """
    Get XML data from HTTP repsonse.
    """
    if response_ok(response):
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.fromstring(response.content, parser=parser)
    else:
        return None


def pretty_json(data):
    """
    Create a pretty formatted JSON string.
    """
    return json.dumps(data, ensure_ascii=False, indent=2)


def pretty_xml(elements):
    """
    Create a pretty formatted XML string.
    """
    return etree.tostring(elements, pretty_print=True).decode()


def tostr_xml(elements):
    """
    Create an XML string.
    """
    return etree.tostring(elements).decode()
