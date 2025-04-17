import uuid
import random
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from cloud_printer import App

app = Flask(__name__)
app.secret_key="flask-must-secure-)q5n3vp2)p%t6x_rj5ksuw9o&$m+nhnt1rqkn$ifv-y1$d^l5j"
bootstrap=Bootstrap5(app)

class SubmitForm(FlaskForm):
    title = StringField('标题：', validators=[DataRequired()])
    content1 = StringField('内容1：', validators=[DataRequired()])
    content2 = StringField('内容2：', validators=[DataRequired()])
    content3 = StringField('内容3：', validators=[DataRequired()])
    content4 = StringField('内容4：', validators=[DataRequired()])
    type = SelectField('类型', choices=[(0, '数字'), (1, '字母'), (2,'混合')], validators=[DataRequired()])
    length = SelectField('位数', choices=[(8, 8), (12, 12), (16,16), (20,20), (24,24)], validators=[DataRequired()])
    qr = StringField('二维码', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/transfer', methods=['GET','POST'])
def transfer():
    form=SubmitForm()
    if request.method == 'GET':
        return render_template('app.html',form=form)
    if request.method == 'POST':
        title = request.form['title']
        content1 = request.form['content1']
        content2 = request.form['content2']
        content3 = request.form['content3']
        content4 = request.form['content4']
        t=int(request.form['type'])
        n=int(request.form['length'])
        qr=request.form['qr']
        cmd=App.generate_cmd(title, [content1, content2, content3, content4], (t,n), qr)
        App.send_print_job(cmd)
        return render_template('app.html', form=form)
