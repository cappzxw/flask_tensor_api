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
api_config = app.config['API']
port_config = app.config['SERVER_PORT']


def make_request_fn():
    request_fn = serving_utils.make_grpc_request_fn(
        servable_name=servable_name_config,
        server=server_config+':'+str(listen_port_config),
        timeout_secs=100
        )
    return request_fn


@ app.route('/translate/'+api_config, methods=['POST'])
def translate():
    inputs = request.form['content']
    outputs = serving_utils.predict([inputs], problem, request_fn)
    outputs, = outputs
    output, score = outputs
    return output[0: output.find('EOS')-1]


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    usr_dir.import_usr_dir(usr_dir_config)
    problem = registry.problem(problem_config)
    hparams = tf.contrib.training.HParams(
        data_dir=os.path.expanduser(data_dir_config)
    )
    problem.get_hparams(hparams)
    request_fn = make_request_fn()
    app.run(
        port=port_config
    )
