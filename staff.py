from flask import Flask, render_template, request
import pymysql.cursors

from appdef import app, conn

@app.route('/staffHome')
def staffHome():
  return render_template('staff.html')

