# shacl tests

## Overview

> Explore python validation of json via `shacl`

Two tests are included:
* test_simple_validation.py:  reproduces  https://shacl.org/playground/ example in python.
* test_clingen_validation.py:  validates clingen example json via their shacl shapes. 

## Setup

```

# setup virtual environment
python3 -m virtualenv --python=python3  venv

. venv/bin/activate

# install dependencies
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

## Run

```

$ python3 -m pytest tests/
================================================================================= test session starts =================================================================================
platform darwin -- Python 3.7.7, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
rootdir: /Users/walsbr/shacl
collected 5 items

tests/test_clingen_validation.py ..                                                                                                                                             [ 40%]
tests/test_simple_validation.py ...                                                                                                                                             [100%]

================================================================================== 5 passed in 4.27s ==================================================================================

```