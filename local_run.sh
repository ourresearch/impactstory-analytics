#!/bin/bash
source venv/bin/activate
python run.py | logger -p local3.debug &
echo "starting analytics"