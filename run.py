import config
config.set_env_vars_from_dot_env()


from impactstoryanalytics import app
app.run(port=5002, debug=False)

