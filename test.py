import unittest
import json
import re
import crawler


# 准备正则表达式
r = re.compile(r"^Python-urllib/3\.[0-9]$")


class TestCrawlerMethods(unittest.TestCase, crawler.Test):
    def test_get(self):
        get = self.get('http://127.0.0.1:8000/test.php', {})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        json_test = json.loads(get['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test,
                         {'HEADER': {'CONNECTION': 'close', 'HOST': '127.0.0.1:8000', 'ACCEPT_ENCODING': 'identity'},
                          'POST': [], 'GET': [], 'COOKIE': []})
        self.assertEqual(get['msg'], "")
        self.assertEqual(get['errmsg'], "")

    def test_get_header(self):
        get = self.get('http://127.0.0.1:8000/test.php', {'header': 'header'})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        json_test = json.loads(get['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test,
                         {'HEADER': {'HEADER': 'header', 'ACCEPT_ENCODING': 'identity', 'HOST': '127.0.0.1:8000',
                                     'CONNECTION': 'close'}, 'COOKIE': [], 'GET': [], 'POST': []})
        self.assertEqual(get['msg'], "")
        self.assertEqual(get['errmsg'], "")

    def test_post(self):
        post = self.post('http://127.0.0.1:8000/test.php', {'post': 'post'}, {})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        json_test = json.loads(post['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test, {'GET': [], 'HEADER': {'HOST': '127.0.0.1:8000', 'CONNECTION': 'close',
                                                           'ACCEPT_ENCODING': 'identity'}, 'COOKIE': [],
                                     'POST': {'post': 'post'}})
        self.assertEqual(post['msg'], "")
        self.assertEqual(post['errmsg'], "")

    def test_post_header(self):
        post = self.post('http://127.0.0.1:8000/test.php', {'post': 'post'}, {'header': 'header'})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        json_test = json.loads(post['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test, {'GET': [], 'HEADER': {'HOST': '127.0.0.1:8000', 'ACCEPT_ENCODING': 'identity',
                                                           'HEADER': 'header', 'CONNECTION': 'close'},
                                     'POST': {'post': 'post'}, 'COOKIE': []})
        self.assertEqual(post['msg'], "")
        self.assertEqual(post['errmsg'], "")

    def test_get_error(self):
        get = self.get('http://127.0.0.1:8000/error.php', {})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        json_test = json.loads(get['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test, {'COOKIE': [], 'POST': [], 'GET': [],
                                     'HEADER': {'ACCEPT_ENCODING': 'identity', 'HOST': '127.0.0.1:8000',
                                                'CONNECTION': 'close'}})
        self.assertFalse(get['msg'] == "")
        self.assertEqual(get['errmsg'], "")

    def test_post_error(self):
        post = self.post('http://127.0.0.1:8000/error.php', {'post': 'post'}, {})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        json_test = json.loads(post['read'])
        self.assertTrue(re.match(r, json_test['HEADER'].pop('USER_AGENT')) is not None)
        self.assertEqual(json_test, {'COOKIE': [], 'POST': {'post': 'post'},
                                     'HEADER': {'HOST': '127.0.0.1:8000', 'CONNECTION': 'close',
                                                'ACCEPT_ENCODING': 'identity'}, 'GET': []})
        self.assertFalse(post['msg'] == "")
        self.assertEqual(post['errmsg'], "")


if __name__ == '__main__':
    unittest.main()
