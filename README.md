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

## References

[1] Chudnov, D., Binkley, P., Frumkin J., Giarlo, M. J., Rylander, M., Singer, R. & Summers, E. (2006). Introducing unAPI. _Ariadne_ 48. http://www.ariadne.ac.uk/issue48/chudnov-et-al/  
[2] https://wiki.k10plus.de/display/K10PLUS/UnAPI
