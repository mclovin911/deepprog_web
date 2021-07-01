from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify

import os
from deepprog_webapps.main_class_apps import MainApps

from threading import Thread
from queue import Queue

from time import sleep

from flask import send_from_directory

import sys
from .step2 import test_instance
from flask import send_file
# """
# /
#   /action
#    |
#    V
#   /wait "Your task id is: xxx. <a href="/result">Result page</a>""
#    |
#    V
#   /result
# """

MAIN_APPS = MainApps()

PATH_TEMPLATE = os.path.split(os.path.abspath(__file__))[0] + '/templates/'
STATIC_FOLDER = os.path.split(os.path.abspath(__file__))[0] + '/static/'

INPUT_QUEUE = Queue()

app = Flask(__name__,
            static_folder='static',
            static_url_path='',
            # template_folder=''
)


@app.route('/downloads/<filename>')
def downloads(filename):
    return send_file('//home/ubuntu/data/DeepProg/matrices/COAD/Step2_COAD/'+filename,as_attachment=True)





"""
@app.route("/<cancer>", methods=['GET', 'POST'])
def cancer_func(cancer):
    if request.method == 'POST':
        omic_dict = dict()
        if 'rna_file' in request.files:
            rna_file = request.files['rna_file']
            if rna_file.filename != '':
                rna_file.save('//home/ubuntu/data/DeepProg/matrices/{0}/upload/{1}'.format(cancer.upper(), rna_file.filename)) 
                omic_dict['RNA'] = 'upload/{0}'.format(rna_file.filename)
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
        return send_file('//home/ubuntu/data/DeepProg/matrices/COAD/Step2_COAD/Step2_COAD_KM_plot_boosting_full.pdf')
        
    if MAIN_APPS.to_reload and MAIN_APPS.reloading:
        MAIN_APPS.to_reload = []
        MAIN_APPS.reloading = False

    return render_template('apps.html', main_apps=MAIN_APPS, cancer=cancer)
"""

### start test space
@app.route("/<cancer>")
def cancer_func(cancer):
    return render_template('apps.html', main_apps=MAIN_APPS, cancer=cancer)

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






### end test space





@app.route("/", methods=['GET', 'POST'])
def main(methods=['GET', 'POST']):
    return render_template('index.html', main_apps=MAIN_APPS)



"""

class DeepProgThreading(Thread):
    """
    """
    def __init__(self, input_queue=INPUT_QUEUE):
        """
        """
        Thread.__init__(self)
        self.input_queue = input_queue
        self.main_apps = MainApps()

    def run(self):
        """
        """
        self._run()

    def _run(self):
        """
        """
        while True:
            if self.input_queue.empty():
                sleep(0.1)
                continue
            try:
                cancer, model, params = self.input_queue.get(True, 0.1)

            except Exception:
                continue

            print('################', cancer, model, params)
            try:
                self.main_apps.cancer_dict[cancer].process_new_dataset(
                    model=model,
                    **params)
            except Exception as e:
                MAIN_APPS.to_reload = True
                MAIN_APPS.logs[cancer].append(
                    'error when predicting {0} using model {1}'.format(
                MAIN_APPS.test_files[cancer]['fname'], model))
                print(e)
            else:
                MAIN_APPS.predicted_any[cancer] = True
                MAIN_APPS.predicted[cancer][model] = MAIN_APPS.predicting[cancer][model]
                MAIN_APPS.predicting[cancer].pop(model)
                MAIN_APPS.to_reload.append(model)

                MAIN_APPS.logs[cancer].append('test dataset {0} predicted using model {1}!'.format(
                    MAIN_APPS.test_files[cancer]['fname'], model))

if __name__ == '__main__':

    THREADING = DeepProgThreading()
    THREADING.daemon = True
    THREADING.start()
    try:
        app.run(host='0.0.0.0', port='8085')
    except KeyboardInterrupt:
        del THREADING

"""