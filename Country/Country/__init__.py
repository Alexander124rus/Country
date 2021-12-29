
"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'se334er4t56yhh78ju'
#app.debug=True
#app.run()


import Country.views


