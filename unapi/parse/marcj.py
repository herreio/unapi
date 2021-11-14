# -*- coding: utf-8 -*-

from ..log import logger

import datetime

from .serialj import SerialJson


class MarcJson(SerialJson):
    """
    Class for parsing MARC JSON (http://format.gbv.de/marc/json)
    """

    def __init__(self, data):
        super().__init__(data)

    def get_ppn(self):
        """
        001: Control Number
        """
        return self.get_value("001", "_", unique=True)

    def get_latest_trans(self):
        """
        005: Date and Time of Latest Transaction
        """
        return self.get_value("005", "_", unique=True)

    def get_latest_trans_datetime(self):
        """
        005: Date and Time of Latest Transaction (as datetime object)
        """
        latest_trans = self.get_latest_trans()
        if latest_trans is not None:
            try:
                return datetime.datetime.strptime(latest_trans, "%Y%m%d%H%M%S.0")
            except ValueError:
                return datetime.datetime.strptime(latest_trans, "%Y%m%d222222:2")

    def get_latest_trans_iso(self):
        """
        005: Date and Time of Latest Transaction (in ISO format)
        """
        latest_trans = self.get_latest_trans_datetime()
        if latest_trans is not None:
            return latest_trans.isoformat()

    def get_data_elements(self):
        """
        008: Fixed-Length Data Elements
        """
        return self.get_value("008", "_", unique=True)

    def get_date_entered(self):
        """
        008: Fixed-Length Data Elements

          00-05 - Date entered on file
        """
        date_elements = self.get_data_elements()
        if len(date_elements) > 5:
            return date_elements[:6]

    def get_date_entered_date(self):
        """
        008: Fixed-Length Data Elements

          00-05 - Date entered on file (as date object)
        """
        date_entered = self.get_date_entered()
        if date_entered is not None:
            return datetime.datetime.strptime(date_entered, "%y%m%d").date()

    def get_date_entered_iso(self):
        """
        008: Fixed-Length Data Elements

          00-05 - Date entered on file (in ISO format)
        """
        date_entered = self.get_date_entered_date()
        if date_entered is not None:
            return date_entered.isoformat()

    def get_holdings_idn(self, occurrence="0"):
        """
        924/DNB: Bestandsinformationen (IDN)
        """
        return self.get_value("924", "a", occurrence=occurrence, repeat=False)

    def get_holdings_isil(self, occurrence="0"):
        """
        924/DNB: Bestandsinformationen (ISIL)
        """
        return self.get_value("924", "b", occurrence=occurrence, repeat=False)

    def get_holdings_from_isil(self, isil, occurrence="0"):
        """
        924/DNB: Bestandsinformationen (IDN)
        """
        isils = self.get_holdings_isil(occurrence=occurrence)
        index = [i for i, s in enumerate(isils) if s == isil]
        if len(index) > 0:
            ppns = self.get_holdings_idn()
            if ppns is not None:
                if len(isils) == len(ppns):
                    return [ppns[i] for i in index]
                else:
                    logger.error("{0}: Unequal number of holding ISILs and PPNs".format(self.name))
