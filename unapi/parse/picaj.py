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

    def get_first_entry_code(self):
        """
        001A/0200: Kennung der Ersterfassung
        """
        return self.get_first_entry().split(":")[0]

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
        return datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date()

    def get_first_entry_date_iso(self):
        """
        001A/0200: Datum der Ersterfassung (in ISO format)
        """
        first_entry_date = self.get_first_entry_date_date()
        return first_entry_date.isoformat()

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
        return datetime.datetime.strptime(change_datetime, "%d-%m-%y %H:%M:%S.%f")

    def get_latest_change_iso(self):
        """
        001B/0210: Zeitstempel der letzten Änderung (in ISO format)
        """
        change_datetime = self.get_latest_change_datetime()
        return change_datetime.isoformat()

    def get_rvk(self, collapse=False):
        """
        045R/5090: Regensburger Verbundklassifikation (RVK)
        """
        return self.get_value("045R", "a", unique=False, repeat=False, collapse=collapse)

    def get_holdings_ppn(self, occurence="01"):
        """
        203@/7800: EPNs der Exemplardaten
        """
        return self.get_value("203@", "0", occurence=occurence, repeat=False)

    def get_holdings_ilns(self, occurence=None):
        """
        101@: ILNs der Exemplardaten
        """
        return self.get_value("101@", "a", occurence=occurence, repeat=False)

    def get_holdings_isil(self, occurence="01"):
        """
        209A/7100: Signatur (Exemplardaten)
          $B    Sigel (nur SWB)

        Das Unterfeld $B wird bei SWB-Bibliotheken im ersten Signaturfeld maschinell belegt.
        """
        return self.get_value("209A", "B", occurence=occurence, repeat=False)

    def get_holdings_isil_occurence(self, occurence="01"):
        """
        209A/7100: Signatur (Exemplardaten)

        Das Unterfeld $B wird bei SWB-Bibliotheken im ersten Signaturfeld maschinell belegt.
        """
        codes = self.get_holdings_isil(occurence=occurence)
        if codes is not None:
            return len(codes)
        else:
            return 0

    def get_holdings_isil_index(self, isil, occurence="01"):
        """
        209A/7100: Signatur (Exemplardaten)
          $B    Sigel (nur SWB)

        Das Unterfeld $B wird bei SWB-Bibliotheken im ersten Signaturfeld maschinell belegt.
        """
        codes = self.get_holdings_isil(occurence=occurence)
        if codes is not None:
            index = [i for i, c in enumerate(codes) if c == isil]
            if len(index) > 0:
                return index

    def get_holdings_from_isil(self, isil, occurence="01"):
        """
        203@/7800: EPNs der Exemplardaten
        209A/7100: Signatur (Exemplardaten)
            $B    Sigel (nur SWB)
        """
        index = self.get_holdings_isil_index(isil, occurence=occurence)
        if index is not None:
            epns = self.get_holdings_ppn(occurence=occurence)
            if epns is not None and len(epns) == self.get_holdings_isil_occurence(occurence=occurence):
                holdings = []
                for i in index:
                    holdings.append(epns[i])
                if len(holdings) > 0:
                    return holdings
            else:
                logger.error("{0}: Unequal number of holding ISILs and PPNs".format(self.name))

    def get_holdings_first_entry_date(self, occurence="01"):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        return self.get_value("201A", "0", occurence=occurence, repeat=False)

    def get_holdings_first_entry_date_date(self, occurence="01"):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        first_entry_date_objs = []
        first_entry_dates = self.get_holdings_first_entry_date(occurence=occurence)
        if first_entry_dates is not None:
            for first_entry_date in first_entry_dates:
                first_entry_date_objs.append(datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date())
            return first_entry_date_objs

    def get_holdings_first_entry_date_iso(self, occurence="01"):
        """
        201A/7902: Datum der Ersterfassung (Exemplardaten)
        """
        first_entry_date_iso = []
        first_entry_dates = self.get_holdings_first_entry_date(occurence=occurence)
        if first_entry_dates is not None:
            for first_entry_date in first_entry_dates:
                first_entry_date_iso.append(datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date().isoformat())
            return first_entry_date_iso

    def get_holdings_latest_change_date(self, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        return self.get_value("201B", "0", occurence=occurence, repeat=False)

    def get_holdings_latest_change_time(self, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        return self.get_value("201B", "t", occurence=occurence, repeat=False)

    def get_holdings_latest_change_str(self, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        latest_change_date = self.get_holdings_latest_change_date(occurence=occurence)
        latest_change_time = self.get_holdings_latest_change_time(occurence=occurence)
        if latest_change_date is not None and latest_change_time is not None:
            if len(latest_change_date) != len(latest_change_time):
                logger.error("{0}: Unequal number of edit dates and times in holding data!".format(self.name))
                return None
            latest_change_str = []
            for i in range(len(latest_change_date)):
                latest_change_str.append("{0} {1}".format(latest_change_date[i], latest_change_time[i]))
            if len(latest_change_str) > 0:
                return latest_change_str

    def get_holdings_latest_change_datetime(self, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (as datetime object)
        """
        change_str = self.get_holdings_latest_change_str(occurence=occurence)
        if change_str is not None:
            latest_change_datetime = []
            for ch_str in change_str:
                if ch_str != "" and ch_str is not None:
                    latest_change_datetime.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f"))
                else:
                    latest_change_datetime.append(ch_str)
            if len(latest_change_datetime) > 0:
                return latest_change_datetime

    def get_holdings_latest_change_iso(self, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (in ISO format)
        """
        change_str = self.get_holdings_latest_change_str(occurence=occurence)
        if change_str is not None:
            latest_change_iso = []
            for ch_str in change_str:
                if ch_str != "" and ch_str is not None:
                    latest_change_iso.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f").isoformat())
                else:
                    latest_change_iso.append(ch_str)
            if len(latest_change_iso) > 0:
                return latest_change_iso

    def get_holdings_isil_latest_change_str(self, isil, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten)
        """
        index = self.get_holdings_isil_index(isil)
        if index is not None:
            isil_latest_change_str = []
            change_str = self.get_holdings_latest_change_str(occurence=occurence)
            if change_str is not None:
                for i in index:
                    isil_latest_change_str.append(change_str[i])
            if len(isil_latest_change_str) > 0:
                return isil_latest_change_str

    def get_holdings_isil_latest_change_datetime(self, isil, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (as datetime object)
        """
        change_str = self.get_holdings_isil_latest_change_str(isil, occurence=occurence)
        if change_str is not None:
            latest_change_datetime = []
            for ch_str in change_str:
                latest_change_datetime.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f"))
            if len(latest_change_datetime) > 0:
                return latest_change_datetime

    def get_holdings_isil_latest_change_iso(self, isil, occurence="01"):
        """
        201B/7903: Datum und Uhrzeit der letzten Änderung (Exemplardaten) (in ISO format)
        """
        change_str = self.get_holdings_isil_latest_change_str(isil, occurence=occurence)
        if change_str is not None:
            latest_change_iso = []
            for ch_str in change_str:
                latest_change_iso.append(datetime.datetime.strptime(ch_str, "%d-%m-%y %H:%M:%S.%f").isoformat())
            if len(latest_change_iso) > 0:
                return latest_change_iso

    def get_holdings_source_first_entry(self, occurence="01"):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten)
        """
        return self.get_value("201D", "0", occurence=occurence, repeat=False)

    def get_holdings_source_first_entry_eln(self, occurence="01"):
        """
        201D/7901: Quelle der Ersterfassung (Exemplardaten)
        """
        source_first_entry = self.get_holdings_source_first_entry(occurence=occurence)
        if source_first_entry is not None:
            codes = []
            for sfe in source_first_entry:
                codes.append(sfe.split(":")[0])
            return codes

    def get_holdings_source_first_entry_date(self, occurence="01"):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten)
        """
        source_first_entry = self.get_holdings_source_first_entry(occurence=occurence)
        if source_first_entry is not None:
            dates = []
            for sfe in source_first_entry:
                dates.append(sfe.split(":")[1])
            if len(dates) > 0:
                return dates

    def get_holdings_source_first_entry_date_date(self, occurence="01"):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten) (as date object)
        """
        source_first_entry_date = self.get_holdings_source_first_entry_date(occurence=occurence)
        if source_first_entry_date is not None:
            dates = []
            for sfe_date in source_first_entry_date:
                dates.append(datetime.datetime.strptime(sfe_date, "%d-%m-%y").date())
        if len(dates) > 0:
            return dates

    def get_holdings_source_first_entry_date_iso(self, occurence="01"):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten) (in ISO format)
        """
        source_first_entry_date = self.get_holdings_source_first_entry_date_date(occurence=occurence)
        if source_first_entry_date is not None:
            dates = []
            for sfe_date in source_first_entry_date:
                dates.append(sfe_date.isoformat())
        if len(dates) > 0:
            return dates

    def get_holdings_eln_first_entry(self, eln, occurence="01"):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten)
        """
        elns = self.get_holdings_source_first_entry_eln(occurence=occurence)
        if elns is not None and eln in elns:
            eln_entries = []
            entries = self.get_holdings_source_first_entry(occurence=occurence)
            if entries is not None:
                eln_entries = [e for e in entries if eln in e]
            if len(eln_entries) > 0:
                return eln_entries

    def get_holdings_eln_first_entry_date(self, eln, occurence="01"):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten)
        """
        first_entry_date = self.get_holdings_eln_first_entry(eln, occurence=occurence)
        if first_entry_date is not None:
            dates = []
            for sfe in first_entry_date:
                dates.append(sfe.split(":")[1])
            if len(dates) > 0:
                return dates

    def get_holdings_eln_first_entry_date_date(self, eln, occurence="01"):
        """
        201D/7901: Datum der Ersterfassung (Exemplardaten) (as date object)
        """
        first_entry_date = self.get_holdings_eln_first_entry_date(eln, occurence=occurence)
        if first_entry_date is not None:
            dates = []
            for sfe_date in first_entry_date:
                dates.append(datetime.datetime.strptime(sfe_date, "%d-%m-%y").date())
        if len(dates) > 0:
            return dates

    def get_holdings_eln_first_entry_date_iso(self, eln, occurence="01"):
        """
        201D/7901: Quelle und Datum der Ersterfassung (Exemplardaten) (in ISO format)
        """
        dates = []
        first_entry_date = self.get_holdings_eln_first_entry_date_date(eln, occurence=occurence)
        if first_entry_date is not None:
            for sfe_date in first_entry_date:
                dates.append(sfe_date.isoformat())
        if len(dates) > 0:
            return dates
