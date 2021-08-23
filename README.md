# `unapi`

This Python package provides a client for retrieving data from unAPIs [1].

## Setup

```sh
# ... via SSH:
pip install -e git+ssh://git@github.com/herreio/unapi.git#egg=unapi
# ... or via HTTPS:
pip install -e git+https://github.com/herreio/unapi.git#egg=unapi
```

## Usage

### Interactive Console

```py
import unapi
client = unapi.Client("https://unapi.k10plus.de", "swb", "ppn")
record = client.request("1132450837", "pp")
```

### Command Line Interface

```sh
unapi --url https://unapi.k10plus.de --db swb --var ppn --record 1132450837 --schema pp
```

## Reference

[1] Chudnov, D., Binkley, P., Frumkin J., Giarlo, M. J., Rylander, M., Singer, R. & Summers E. (2006). Introducing unAPI. _Ariadne_ 48. http://www.ariadne.ac.uk/issue48/chudnov-et-al/
