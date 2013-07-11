from impactstoryanalytics import app
import os


# set all the environmental variables defined in the .env list
with open(".env", "r") as f:
    str = f.read()

for line in str.split("\n"):
    try:
        key, val = line.split("=")
        os.environ[key] = val
    except ValueError:
        continue  # line wasn't a value assignment, move on


app.run(port=5002, debug=True)
