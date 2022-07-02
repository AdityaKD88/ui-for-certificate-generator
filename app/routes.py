import os
from re import template
import pandas as pd
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for, redirect, flash
app = Flask(__name__)
app.secret_key = 'you-will-never-guess'

def certificate_generator(name,grade,course_name,course_dur,registration):
    pass

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv','xlsx'}

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="POST":
        form = request.form
        name = form.get('name')
        grade = form.get('grade')
        course_name = form.get('course_name')
        course_dur = form.get('course_dur')
        registration = form.get('registration')
        department = form.get('dep')
        
        if department==0:
            dep="Information Technology"
            return dep
        elif department==1:
            dep="Digital Marketing"
            return dep
        #print(name,grade,course_name,course_dur,registration,dep)
        result = certificate_generator(name,grade,course_name,course_dur,registration,dep)
        return render_template('index.html')
    return render_template('index.html')

@app.route('/upload_file',methods=['GET','POST'])
def upload_file():
    if request.method=="POST":
        if 'file' not in request.files:
            flash('No file uploaded','danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no file selected','danger')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            path=os.path.join(os.getcwd(),"app/static/uploads/", filename )
            file.save(path)
            df=pd.read_excel(path)
            for i, r in df.iterrows():
                if r['generated'] != 1:
                    result = certificate_generator(r['Name'].capitalize(), r['Grade'], 
                                r['Course Name'].title(), r['Course Duration'],r['Registration No.'])
            return redirect(request.url)
    return render_template('upload_file.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)