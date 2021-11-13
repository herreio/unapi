# -*- coding: utf-8 -*-

from ..log import logger


class SerialJson:
    """
    Generic class for parsing MARC JSON or PICA JSON
    """

    def __init__(self, data):
        self.data = data
        self.idx = self._indices()
        self.name = type(self).__name__

    def _indices(self):
        indices = {}
        for i, field in enumerate(self.data):
            if field[0] in indices:
                indices[field[0]].append(i)
            else:
                indices[field[0]] = [i]
        return indices

    def _field_pos(self, name):
        if name in self.idx:
            return self.idx[name]

    def get_field(self, name, unique=False):
        found = []
        positions = self._field_pos(name)
        if positions is not None:
            for i in positions:
                found.append(self.data[i])
        if unique:
            if len(found) == 1:
                return found[0]
            else:
                logger.warning("{0}: Expected field {1} to be unique. Found {2} occurences.".format(self.name, name, len(found)))
        if len(found) > 0:
            return found

    @staticmethod
    def _subfield_pos(row, subf):
        positions = []
        for i, val in enumerate(row):
            if val == subf:
                positions.append(i + 1)
        if len(positions) > 0:
            return positions

    def _value_from_row(self, row, subfield, repeat=True):
        pos = self._subfield_pos(row, subfield)
        if pos is not None:
            if len(pos) == 1:
                return row[pos[0]]
            else:
                if not repeat:
                    if all(len(row[p]) == 1 for p in pos):
                        return [row[p][0] for p in pos]
                    else:
                        logger.warning("{0}: Expected unrepeated subfield {1} in field {2}. Found mutiple occurences.".format(self.name, subfield, row[0]))
                return [row[p] for p in pos]

    def _value_from_rows(self, rows, subfield, repeat=True, collapse=False):
        found = []
        for row in rows:
            sub_found = []
            pos = self._subfield_pos(row, subfield)
            if pos is not None:
                for p in pos:
                    sub_found.append(row[p])
            if collapse:
                sub_found = "|".join(sub_found)
            if len(sub_found) > 0:
                found.append(sub_found)
        if len(found) > 0:
            if collapse:
                return "||".join(found)
            if not repeat:
                if not all(len(sbf) == 1 for sbf in found):
                    logger.warning("{0}: Expected unrepeated subfield {1} in field {2}. Found mutiple occurences.".format(self.name, subfield, rows[0][0]))
                return [sbf[0] for sbf in found]
            return found
        else:
            logger.error("{0}: Subfield {1} not found in field {2}!".format(self.name, subfield, rows[0][0]))

    def get_value(self, field, subfield, unique=False, repeat=True, collapse=False):
        found = self.get_field(field, unique=unique)
        if found is not None:
            if unique and type(found[0]) != list:
                return self._value_from_row(found, subfield, repeat=repeat)
            else:
                return self._value_from_rows(found, subfield, repeat=repeat, collapse=collapse)
        else:
            logger.error("{0}: Field {1} not found!".format(self.name, field))
