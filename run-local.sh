#!/bin/bash
source venv/bin/activate
python run.py | logger &
echo "starting analytics"