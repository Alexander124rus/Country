"""
This script runs the Country application using a development server.
"""

from os import environ
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


import sqlite3 as sql
from Country import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
