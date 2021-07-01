from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import os
from flask import send_from_directory
import sys
from .step2 import test_instance
from flask import send_file


PATH_TEMPLATE = os.path.split(os.path.abspath(__file__))[0] + '/templates/'
STATIC_FOLDER = os.path.split(os.path.abspath(__file__))[0] + '/static/'

app = Flask(__name__,
            static_folder='static',
            static_url_path='',
)


@app.route('/downloads/<filename>')
def downloads(filename):
    return send_file('//home/ubuntu/data/DeepProg/matrices/COAD/Step2_COAD/'+filename,as_attachment=True)

@app.route("/<cancer>")
def cancer_func(cancer):
    return render_template('apps.html', cancer=cancer)

@app.route("/get_result", methods=['GET', 'POST'])                      
def get_result():                        
    try:
        omic_dict = dict()
        app.logger.warning(request.form['cancer_type'])
        app.logger.warning(request.form)
        app.logger.warning(request.files)
        if 'rna_file' in request.files:
            rna_file = request.files['rna_file']
            if rna_file.filename != '':
                app.logger.warning(list(os.listdir('.')))
                rna_file.save('data/DeepProg/matrices/COAD/upload/{0}'.format(rna_file.filename)) 
                app.logger.warning('here1')
                omic_dict['RNA'] = 'upload/{0}'.format(rna_file.filename)
                app.logger.warning('saved') 
        if 'mir_file' in request.files:
            mir_file = request.files['mir_file']
            if mir_file.filename != '':
                mir_file.save('//home/ubuntu/data/DeepProg/matrices/{0}/upload/{1}'.format(cancer.upper(), mir_file.filename)) 
                omic_dict['MIR'] = 'upload/{0}'.format(mir_file.filename)
        if 'meth_file' in request.files:
            meth_file = request.files['meth_file']
            if meth_file.filename != '':
                meth_file.save('//home/ubuntu/data/DeepProg/matrices/{0}/upload/{1}'.format(cancer.upper(), meth_file.filename)) 
                omic_dict['METH'] = 'upload/{0}'.format(meth_file.filename)
        test_name = request.form['test_name']
        test_instance(omic_dict, test_name)
        results = list(os.listdir("//home/ubuntu/data/DeepProg/matrices/COAD/Step2_COAD"))
        return jsonify(results=results)
    except Exception as e:
        return str(e)


@app.route("/", methods=['GET', 'POST'])
def main(methods=['GET', 'POST']):
    return render_template('index.html', main_apps=MAIN_APPS)
