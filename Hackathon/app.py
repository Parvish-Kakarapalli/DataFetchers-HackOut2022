from cProfile import label
from crypt import methods
from curses import KEY_FIND
from distutils import extension
from fileinput import filename
import os
import io
import base64
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from pkgutil import ImpImporter
import re
from flask import Flask, flash, request, redirect, url_for, render_template, session, send_file, Response, make_response
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
from functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           





@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        session['l'] = request.form['label']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session["name"]=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('select'))
            # return "Uploaded!"
        
    return render_template('index.html')



@app.route('/select', methods = ['GET', 'POST'])
def select():
    df = pd.read_csv(session['name'])
    col = num_cols(df, session['l'])
    session["cols"] = col
    return render_template('test.html', cols = col)    



@app.route('/scat', methods = ["GET", "POST"])
def scat():
    col = session["cols"]
    if request.method == "POST":
        
        session['f1'] = request.form['f1']
        session['f2'] = request.form['f2']
        df = pd.read_csv(session['name'])
        df = process(df, session['l'])
        
        if 'f1' in session and 'f2' in session:
            bytes_obj  = do_plot(df, session['f1'], session['f2'], 'labels')
            return send_file(bytes_obj, mimetype = 'image/png')
            
            
    return render_template('scat.html', cols = col)


@app.route('/hist', methods = ["GET", "POST"])
def hist():
    col = session["cols"]
    if request.method == "POST":
        
        session['f'] = request.form['f']
        df = pd.read_csv(session['name'])
        df = process(df, session['l'])
        if 'f' in session:
            bytes_obj  = do_hist(df, session['f'], 'labels')
            return send_file(bytes_obj, mimetype = 'image/png')
            
            
    return render_template('hist.html', cols = col)


@app.route('/box', methods = ["GET", "POST"])
def box():
    col = session["cols"]
    if request.method == "POST":
        session['b'] = request.form['b']
        df = pd.read_csv(session['name'])
        
        df = process(df, session['l'])
        if 'b' in session:
            bytes_obj  = do_box(df, session['b'], 'labels')
            return send_file(bytes_obj, mimetype = 'image/png')
            
            
    return render_template('box.html', cols = col)


@app.route('/pdf', methods = ["GET", "POST"])
def pdf():
    col = session["cols"]
    if request.method == "POST":
        session['pdf'] = request.form['pdf']
        df = pd.read_csv(session['name'])
        df = process(df, session['l'])
        if 'pdf' in session:
            bytes_obj  = do_pdf(df, session['pdf'], 'labels')
            return send_file(bytes_obj, mimetype = 'image/png')
            
            
    return render_template('pdf.html', cols = col)

@app.route('/cdf', methods = ["GET", "POST"])
def cdf():
    col = session["cols"]
    if request.method == "POST":
        session['cdf'] = request.form['cdf']
        df = pd.read_csv(session['name'])
        df = process(df, session['l'])
        if 'cdf' in session:
            bytes_obj  = do_cdf(df, session['cdf'], 'labels')
            return send_file(bytes_obj, mimetype = 'image/png')
            
            
    return render_template('cdf.html', cols = col)

@app.route('/tsne')
def ts():
    col = session["cols"]
    df = pd.read_csv(session['name'])
    df = process(df, session['l'])
    lab = df['labels']
    df = std_data(df)
    df = tsne(df, lab)
    # df = df.to_json()
    bytes_obj  = do_plot(df, 'feature 1', 'feature 2', 'labels')
    return send_file(bytes_obj, mimetype = 'image/png')
            
            

if __name__ == '__main__':
    app.run(debug = True)