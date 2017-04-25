from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/staffHome')
def staffHome():
  return render_template('staff.html')