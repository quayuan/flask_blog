from flask import Flask

import logging
from logging import handlers
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor


def create_flask_app(config, enable_config_file=False):
    """
    创建Flask应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(config)
    if enable_config_file:
        from utils import constants
        app.config.from_envvar(constants.GLOBAL_SETTING_ENV_NAME, silent=True)

    return app


def create_app(config, enable_config_file=False):
    """
    创建应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: 应用
    """
    app = create_flask_app(config, enable_config_file)

    # ----- To configure the log begin----- #
    logging_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    th = logging.handlers.TimedRotatingFileHandler(filename=app.config.get('LOG_PATH'),
                                                   interval=1,
                                                   when='D',
                                                   backupCount=7,
                                                   encoding='utf-8')
    th.setFormatter(fmt=logging_formatter)
    app.logger.setLevel(app.config.get('LOG_LEVEL'))
    app.logger.addHandler(th)

    # ----- To configure the log end----- #

    # ---- Configure scheduler begin -----#

    """
    创建定时任务工具对象
    
    将scheduler对象保存到flask app对象中的目的，是方便视图执行的时候随时产生新的定时任务需求，
    可以借助current_app.scheduler.add_job()来动态添加新的定时任务
    """
    executors = {
        'default': ThreadPoolExecutor(10),
    }

    app.scheduler = BackgroundScheduler(executors=executors)

    from .schedule import test_task

    # 定时任务
    app.scheduler.add_job(test_task.test, 'cron', hour='0, 12', minute='35', args=[app])

    # 启动立即执行任务
    app.scheduler.add_job(test_task.test, 'date', args=[app])

    app.scheduler.start()

    # ---- Configure scheduler end -----#
