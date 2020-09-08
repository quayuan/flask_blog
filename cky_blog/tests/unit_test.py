import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))
sys.path.insert(0, BASE_DIR)

import json
import unittest

from cky_blog import create_app
from common.settings.testing import TestingConfig


class TestResources(unittest.TestCase):
    """
    先留个位置，要测的时候再写
    """

    def set_up(self):
        """
        测试方法初始化函数
        使flask处于测试模式：
            flask 添加配置项：TESTING=True
        :return:
        """
        app = create_app(TestingConfig)
        self.client = app.test_client()

    def test_normal_requests(self):
        """
        测试正常接口情况
        :return:
        """
        respon = self.client.get('')

        # judge response status code
        self.assertEqual(respon.status_code, 200)

        # judge if the response data is JSON
        respon_dict = json.loads(respon.data)

        # assert 'msg' in response data
        self.assertIn('msg', respon_dict)


if __name__ == '__main__':
    unittest.main()
