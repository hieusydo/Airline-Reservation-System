#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn
import register
import login
import publicinfo
import customer
import agent
import staff

#Define a route to hello function
@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
  username = session['username']
  cursor = conn.cursor();
  blog = request.form['blog']
  query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
  cursor.execute(query, (blog, username))
  conn.commit()
  cursor.close()
  return redirect(url_for('home'))

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')
    
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
