import MySQLdb
from flask import Flask, render_template
conn = MySQLdb.connect("Hostname","dbusername","password","dbname")
cursor = conn.cursor()
def example():
    cursor.execute("select * from Book")
    data = cursor.fetchall() #data from database
    return render_template("search.html", value=data)