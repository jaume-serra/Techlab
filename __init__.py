
# coding: utf-8
# #!/usr/bin/python

from flask import Flask


app = Flask(__name__)


from routes import *

from apirest import apirest as apirest_blueprint
app.register_blueprint(apirest_blueprint)

app.run(host="0.0.0.0")
