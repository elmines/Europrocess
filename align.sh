#!/bin/bash

rm -rf train/ "test"/
python3 align.py --source ../txt --train train --test "test" --langs es en
