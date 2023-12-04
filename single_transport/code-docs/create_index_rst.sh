#!/bin/bash

head -n 18 index_template.rst > index.rst
ls source/modules/ | sed 's/^/   /' |  sed -e 's/\.rst$//' >> index.rst
tail -n 10 index_template.rst >> index.rst

