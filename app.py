from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from tensor2tensor.serving import serving_utils
from tensor2tensor.utils import registry
from tensor2tensor.utils import usr_dir
from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
servable_name_config = app.config['SERVABLE_NAME']
server_config = app.config['SERVER']
listen_port_config = app.config['LISTEN_PORT']
usr_dir_config = app.config['USR_DIR']
problem_config = app.config['PROBLEM']
data_dir_config = app.config['DATA_DIR']
port_config = app.config['SERVER_PORT']
language_config = app.config['LANGUAGE']


class Lang:
    def __init__(self, name, usrdir, datadir, pro):
        self.problem = self.make_problem_fn(usrdir, datadir, pro)
        self.request = self.make_request_fn(name)

    def make_request_fn(self, name):
        request_fn = serving_utils.make_grpc_request_fn(
            servable_name=name,
            server=server_config+':'+str(listen_port_config),
            timeout_secs=100
            )
        return request_fn

    def make_problem_fn(self, usrdir, datadir, pro):
        tf.logging.set_verbosity(tf.logging.INFO)
        usr_dir.import_usr_dir(usrdir)
        problem = registry.problem(pro)
        hparams = tf.contrib.training.HParams(
            data_dir=os.path.expanduser(datadir)
        )
        problem.get_hparams(hparams)
        return problem


@ app.route('/translate/mn-zh', methods=['POST'])
def translate_mn():
    inputs = request.form['content']
    outputs = serving_utils.predict([inputs], lang_list['mn'].problem, lang_list['mn'].request)
    outputs, = outputs
    output, score = outputs
    return output[0: output.find('EOS')-1]


@ app.route('/translate/uy-zh', methods=['POST'])
def translate_uy():
    inputs = request.form['content']
    outputs = serving_utils.predict([inputs], lang_list['uy'].problem, lang_list['uy'].request)
    outputs, = outputs
    output, score = outputs
    return output[0: output.find('EOS')-1]


if __name__ == '__main__':
    lang_list = {}

    for i in range(len(language_config)):
        name = servable_name_config[i]
        usrdir = usr_dir_config[i]
        datadir = data_dir_config[i]
        pro = problem_config[i]
        language = language_config[i]
        lang = Lang(name, usrdir, datadir, pro)
        lang_list[language] = lang

    app.run(
        port=port_config
    )
