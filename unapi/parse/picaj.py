# -*- coding: utf-8 -*-

import datetime

from .serialj import SerialJson


class PicaJson(SerialJson):
    """
    Class for parsing PICA JSON (http://format.gbv.de/pica/json)
    """

    def __init__(self, data):
        super().__init__(data)

    def get_ppn(self):
        """
        003@/0100: Pica-Produktionsnummer
        """
        return self.get_value("003@", "0", unique=True)

    def get_first_entry(self):
        """
        001A/0200: Kennung und Datum der Ersterfassung
        """
        return self.get_value("001A", "0", unique=True)

    def get_first_entry_date(self):
        """
        001A/0200: Datum der Ersterfassung
        """
        return self.get_first_entry().split(":")[1]

    def get_first_entry_date_date(self):
        """
        001A/0200: Datum der Ersterfassung (as date object)
        """
        first_entry_date = self.get_first_entry_date()
        if first_entry_date is not None:
            return datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date()

    def get_first_entry_date_iso(self):
        """
        001A/0200: Datum der Ersterfassung (in ISO format)
        """
        first_entry_date = self.get_first_entry_date_date()
        if first_entry_date is not None:
            return first_entry_date.isoformat()

    def get_first_entry_code(self):
        """
        001A/0200: Kennung der Ersterfassung
        """
        return self.get_first_entry().split(":")[0]

    def get_latest_change(self):
        """
        001B/0210: Kennung und Datum der letzten Änderung
        """
        return self.get_value("001B", "0", unique=True, repeat=False)

    def get_latest_change_code(self):
        """
        001B/0210: Kennung der letzten Änderung
        """
        return self.get_latest_change().split(":")[0]

    def get_latest_change_date(self):
        """
        001B/0210: Datum der letzten Änderung
        """
        return self.get_latest_change().split(":")[1]

    def get_latest_change_time(self):
        """
        001B/0210: Uhrzeit der letzten Änderung
        """
        return self.get_value("001B", "t", unique=True, repeat=False)

    def get_latest_change_str(self):
        """
        001B/0210: Zeitstempel der letzten Änderung
        """
        d = self.get_latest_change_date()
        t = self.get_latest_change_time()
        return "{0} {1}".format(d, t)

    def get_latest_change_datetime(self):
        """
        001B/0210: Zeitstempel der letzten Änderung (as datetime object)
        """
        change_datetime = self.get_latest_change_str()
        if change_datetime is not None:
            return datetime.datetime.strptime(change_datetime, "%d-%m-%y %H:%M:%S.%f")

    def get_latest_change_iso(self):
        """
        001B/0210: Zeitstempel der letzten Änderung (in ISO format)
        """
        change_datetime = self.get_latest_change_datetime()
        if change_datetime is not None:
            return change_datetime.isoformat()

    def get_rvk(self, collapse=False):
        """
        045R/5090: Regensburger Verbundklassifikation (RVK)
        """
        return self.get_value("045R", "a", unique=False, repeat=False, collapse=collapse)
