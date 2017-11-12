import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import plan

UPLOAD_FOLDER = 'Planilhas'
EXTENSION = set(['csv'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSION

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        print('Entrou')
        print(request.files)
        file = request.files.get('planilha')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
            fieldnames, linhas_com_risco_ordenadas = plan.recebe_plan(filename)
            os.remove(filename)
        return render_template('table.html', fieldnames=fieldnames, result_dict=linhas_com_risco_ordenadas)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result')
def result():
	return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
