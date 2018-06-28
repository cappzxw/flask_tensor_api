# flask_fensor_api
## 基于t2t的多语言翻译api框架

将训练好的t2t模型加载到内存并开启restful_api
## 准备
- python2, tensorflow, tensor2tensor
- [安装配置tensorflow-serving](https://www.tensorflow.org/serving/setup#installing_the_modelserver)
- 将t2t模型导出，与训练目录下的`/self_script`和`/self_data`上传服务器指定目录(`/t2t`)
    ```
    t2t-exporter \
    --t2t_usr_dir=self_script \
    --problems=my_problem --data_dir=./self_data \ 
    --model=lstm_seq2seq_attention \
    --hparams_set=lstm_attention \
    --output_dir=./train
    ```
- 开启tensorflow-server<br>
    ```
    tensorflow_model_server \
    --port=9000 \
    --model_name=lstm_seq2seq_attention \
    --model_base_path=~/self_t2t/train/export/Servo
    ```
- 安装tensorflow-serving-api<br>
`install tensorflow-serving-api`

## 开启api
- 下载flask_tensor_api到指定目录(`/t2t`)
- 编辑config.py文件
    ```
    # server configuration
    SERVER = '127.0.0.1'
    LISTEN_PORT = 监听开启的tensorflow-server的端口(9000)
    SERVER_PORT = flask的端口(默认5000)
    # tensor configuration
    SERVABLE_NAME = 'lstm_seq2seq_attention'
    USR_DIR = self_script路径
    PROBLEM = 定义的problem名字
    DATA_DIR = self_data路径
    # api configuration
    API = 源语言到目标语言(mn-zh)
    ```
- 启动服务 `python app.py`


### 参考
> https://blog.csdn.net/csa121/article/details/79605215

> https://github.com/tensorflow/tensor2tensor/blob/82726e2708f7dd88abdd7c484c5cb7bb86cf7ede/tensor2tensor/serving/README.md

> https://spacewander.github.io/explore-flask-zh/5-configuration.html

