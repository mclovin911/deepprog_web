from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify

from os.path import abspath
from os.path import split as pathsplit

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

PATH_TEMPLATE = pathsplit(abspath(__file__))[0] + '/templates/'
STATIC_FOLDER = pathsplit(abspath(__file__))[0] + '/static/'

INPUT_QUEUE = Queue()

app = Flask(__name__,
            static_folder='static',
            static_url_path='',
            # template_folder=''
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('{0}/{1}'.format(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route("/action/<cancer>", methods=['GET', 'POST'])
def action(cancer):
    """
    """
    args = request.form
    test_tsv = {args['data type']: args['data files']}
    survival_tsv = args['survival files']
    fname = args['data name']
    MAIN_APPS.test_files[cancer] = {'test_tsv': test_tsv,
                                    'test_survival': survival_tsv,
                                    'fname': fname}
    MAIN_APPS.ready_to_test[cancer] = True

    MAIN_APPS.logs[cancer].append('test dataset {0} loaded!'.format(fname))
    print('########  ########')

    return redirect(cancer)

@app.route("/predict/<cancer>/<model>", methods=['GET', 'POST'])
def predict(cancer, model):
    """
    """
    MAIN_APPS.predicting[cancer][model] = MAIN_APPS.test_files[cancer]['fname']
    INPUT_QUEUE.put((cancer, model, MAIN_APPS.test_files[cancer]))

    print('########  PREDICTING ########')
    MAIN_APPS.logs[cancer].append('predicting {0} using model {1}'.format(
        MAIN_APPS.test_files[cancer]['fname'], model))

    MAIN_APPS.reload_logs = True

    return jsonify({'predict':True})

@app.route("/predicted/<cancer>", methods=['GET', 'POST'])
def predicted(cancer):
    """
    """
    reload_logs = MAIN_APPS.reload_logs

    if MAIN_APPS.to_reload:
        MAIN_APPS.reloading = True
        reload_logs = True

    json = jsonify({
        'reload_logs': reload_logs,
        'reload': MAIN_APPS.to_reload})

    MAIN_APPS.reload_logs = False
    MAIN_APPS.to_reload = []

    return json

@app.route("/<cancer>", methods=['GET', 'POST'])
def cancer_func(cancer):
    if request.method == 'POST':
        rna_file = request.form['rna_file']
        rna_file.save(rna_file.filename)
        mir_file = request.form['mir_file']
        meth_file = request.form['meth_file']
        test_name = request.form['test_name']
        OMIC_file = {'RNA': rna_file, 'METH': meth_file, 'MIR': mir_file}
        test_instance(OMIC_file, test_name)
        print('hello world', file=sys.stderr)
        return send_file('//home/ubuntu/code/DeepProg/examples/data/Step2/Step2_KM_plot_boosting_full.pdf')
        
    if MAIN_APPS.to_reload and MAIN_APPS.reloading:
        MAIN_APPS.to_reload = []
        MAIN_APPS.reloading = False

    return render_template('apps.html', main_apps=MAIN_APPS, cancer=cancer)

@app.route("/", methods=['GET', 'POST'])
def main(methods=['GET', 'POST']):
    """
    """
    return render_template('index.html', main_apps=MAIN_APPS)


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
