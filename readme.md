# flask_fensor_api
## 基于t2t的多语言翻译api框架

将训练好的t2t模型加载到内存并开启api服务
## 准备
- python2, tensorflow, tensor2tensor, flask-cors
- [安装配置tensorflow-serving](https://www.tensorflow.org/serving/setup#installing_the_modelserver)
- 将t2t模型导出，与训练目录下的`/self_script`和`/self_data`上传服务器指定目录
    ```
    t2t-exporter \
    --t2t_usr_dir=self_script \
    --problems=my_problem --data_dir=./self_data \ 
    --model=lstm_seq2seq_attention \
    --hparams_set=lstm_attention \
    --output_dir=./train
    ```
- 开启tensorflow-server
    ```
    tensorflow_model_server \
    --port=9000 \
    --model_name=yourname \
    --model_base_path=~/self_t2t/train/export/Servo
    ```
    OR `tensorflow_model_server –model_config_file=models.json –port=9000`
- 安装tensorflow-serving-api
`install tensorflow-serving-api`

## 开启api
- 下载flask_tensor_api到指定目录
- 编辑conf.py文件
- 启动服务 `gunicorn -c run.py  app:app -p ./log/web.pid -D`

- 查看服务 `cat ./log/web.pid`


### 参考
> https://blog.csdn.net/csa121/article/details/79605215

> https://github.com/tensorflow/tensor2tensor/blob/82726e2708f7dd88abdd7c484c5cb7bb86cf7ede/tensor2tensor/serving/README.md

> https://spacewander.github.io/explore-flask-zh/5-configuration.html

> http://www.pythondoc.com/exploreflask/deployment.html
