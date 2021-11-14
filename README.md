# `unapi`

This Python package provides a unAPI client [1] for retrieving data from K10plus [2].

## Setup

```sh
# ... via SSH:
pip install -e git+ssh://git@github.com/herreio/unapi.git#egg=unapi
# ... or via HTTPS:
pip install -e git+https://github.com/herreio/unapi.git#egg=unapi
```

## Usage

### Command Line Interface

```sh
unapi --id 1132450837 --format pp
```

### Interactive Console

```py
import unapi
client = unapi.Client()
record = client.request("1132450837", "pp")
```

#### Parse Response

```py
# import parser class, PicaJson and MarcJson are available
from unapi import PicaJson
# request format picajson (default: pp)
record = client.request("1132450837", "picajson")
# create parser instance
record_pica = PicaJson(record)
# parse first entry field
first_entry = record_pica.get_value("001A", "0", unique=True)
first_entry_eln = first_entry.split(":")[0]
first_entry_date = first_entry.split(":")[1]
# parse first entry date
import datetime
first_entry_date_obj = datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date()
first_entry_date_iso = first_entry_date_obj.isoformat()
```

## References

[1] Chudnov, D., Binkley, P., Frumkin J., Giarlo, M. J., Rylander, M., Singer, R. & Summers, E. (2006). Introducing unAPI. _Ariadne_ 48. http://www.ariadne.ac.uk/issue48/chudnov-et-al/  
[2] https://wiki.k10plus.de/display/K10PLUS/UnAPI
