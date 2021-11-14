# -*- coding: utf-8 -*-

from ..log import logger

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

    def get_holdings_ppn(self):
        return self.get_value("203@", "0", repeat=False)

    def get_holdings_ilns(self):
        return self.get_value("101@", "a", repeat=False)

    def get_holdings_first_entry_date(self):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        return self.get_value("201A", "0", repeat=False)

    def get_holdings_first_entry_date_date(self):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        first_entry_date_objs = []
        first_entry_dates = self.get_holdings_first_entry_date()
        for first_entry_date in first_entry_dates:
            first_entry_date_objs.append(datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date())
        return first_entry_date_objs

    def get_holdings_first_entry_date_iso(self):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        first_entry_date_iso = []
        first_entry_dates = self.get_holdings_first_entry_date()
        for first_entry_date in first_entry_dates:
            first_entry_date_iso.append(datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date().isoformat())
        return first_entry_date_iso

    def get_holdings_latest_change_date(self):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        return self.get_value("201B", "0", repeat=False)

    def get_holdings_latest_change_time(self):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        return self.get_value("201B", "t", repeat=False)

    def get_holdings_latest_change_str(self):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        latest_change_str = []
        latest_change_date = self.get_holdings_latest_change_date()
        latest_change_time = self.get_holdings_latest_change_time()
        if len(latest_change_date) != len(latest_change_time):
            logger.error("{0}: Unequal number of edit dates and times in holding data!".format(self.name))
            return None
        for i in range(len(latest_change_date)):
            latest_change_str.append("{0} {1}".format(latest_change_date[i], latest_change_time[i]))
        return latest_change_str

    def get_holdings_latest_change_datetime(self):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (as datetime object)
        """
        latest_change_datetime = []
        change_str = self.get_holdings_latest_change_str()
        for ch_str in change_str:
            if ch_str is not None:
                latest_change_datetime.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f"))
            else:
                latest_change_datetime.append(ch_str)
        return latest_change_datetime

    def get_holdings_latest_change_iso(self):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (in ISO format)
        """
        latest_change_iso = []
        change_str = self.get_holdings_latest_change_str()
        for ch_str in change_str:
            if ch_str is not None:
                latest_change_iso.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f").isoformat())
            else:
                latest_change_iso.append(ch_str)
        return latest_change_iso

    def get_holdings_source_first_entry(self):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten)
        """
        return self.get_value("201D", "0", repeat=False)

    def get_holdings_source_first_entry_eln(self):
        """
        201D/7901: Quelle der Ersterfassung (Exemplardaten)
        """
        codes = []
        source_first_entry = self.get_holdings_source_first_entry()
        for sfe in source_first_entry:
            codes.append(sfe.split(":")[0])
        return codes

    def get_holdings_source_first_entry_date(self):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten)
        """
        dates = []
        source_first_entry = self.get_holdings_source_first_entry()
        for sfe in source_first_entry:
            dates.append(sfe.split(":")[1])
        return dates

    def get_holdings_source_first_entry_date_date(self):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten) (as date object)
        """
        first_entry_date = self.get_holdings_source_first_entry_date()
        if first_entry_date is not None:
            return datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date()

    def get_holdings_source_first_entry_date_iso(self):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten) (in ISO format)
        """
        first_entry_date = self.get_holdings_source_first_entry_date_date()
        if first_entry_date is not None:
            first_entry_date.isoformat()
