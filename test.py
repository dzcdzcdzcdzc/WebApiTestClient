import unittest
import json
import crawler

__author__ = 'zhichen.dai'


class TestCrawlerMethods(unittest.TestCase, crawler.Test):
    def test_get(self):
        get = self.get('http://127.0.0.1:8000/test/test.php', {})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        self.assertEqual(json.loads(get['read']), {'COOKIE': [], 'POST': [], 'GET': [],
                                                   'HEADER': {'ACCEPT_ENCODING': 'identity', 'HOST': '127.0.0.1:8000',
                                                              'USER_AGENT': 'Python-urllib/3.4',
                                                              'CONNECTION': 'close'}})
        self.assertEqual(get['msg'], "")
        self.assertEqual(get['errmsg'], "")

    def test_get_header(self):
        get = self.get('http://127.0.0.1:8000/test/test.php', {'header': 'header'})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        self.assertEqual(json.loads(get['read']), {'GET': [], 'COOKIE': [], 'POST': [],
                                                   'HEADER': {'HEADER': 'header', 'CONNECTION': 'close',
                                                              'HOST': '127.0.0.1:8000', 'ACCEPT_ENCODING': 'identity',
                                                              'USER_AGENT': 'Python-urllib/3.4'}})
        self.assertEqual(get['msg'], "")
        self.assertEqual(get['errmsg'], "")

    def test_post(self):
        post = self.post('http://127.0.0.1:8000/test/test.php', {'post': 'post'}, {})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        self.assertEqual(json.loads(post['read']), {'POST': {'post': 'post'},
                                                    'HEADER': {'CONNECTION': 'close', 'ACCEPT_ENCODING': 'identity',
                                                               'USER_AGENT': 'Python-urllib/3.4',
                                                               'HOST': '127.0.0.1:8000'}, 'COOKIE': [], 'GET': []})
        self.assertEqual(post['msg'], "")
        self.assertEqual(post['errmsg'], "")

    def test_post_header(self):
        post = self.post('http://127.0.0.1:8000/test/test.php', {'post': 'post'}, {'header': 'header'})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        self.assertEqual(json.loads(post['read']), {'POST': {'post': 'post'},
                                                    'HEADER': {'ACCEPT_ENCODING': 'identity', 'CONNECTION': 'close',
                                                               'HOST': '127.0.0.1:8000', 'HEADER': 'header',
                                                               'USER_AGENT': 'Python-urllib/3.4'}, 'COOKIE': [],
                                                    'GET': []})
        self.assertEqual(post['msg'], "")
        self.assertEqual(post['errmsg'], "")

    def test_get_error(self):
        get = self.get('http://127.0.0.1:8000/test/error.php', {})
        self.assertTrue(isinstance(get, dict))
        self.assertEqual(get['error'], 0)
        self.assertEqual(json.loads(get['read']), {'COOKIE': [], 'POST': [], 'GET': [],
                                                   'HEADER': {'ACCEPT_ENCODING': 'identity', 'HOST': '127.0.0.1:8000',
                                                              'USER_AGENT': 'Python-urllib/3.4',
                                                              'CONNECTION': 'close'}})
        self.assertFalse(get['msg'] == "")
        self.assertEqual(get['errmsg'], "")

    def test_post_error(self):
        post = self.post('http://127.0.0.1:8000/test/error.php', {'post': 'post'}, {})
        self.assertTrue(isinstance(post, dict))
        self.assertEqual(post['error'], 0)
        self.assertEqual(json.loads(post['read']), {'POST': {'post': 'post'},
                                                    'HEADER': {'CONNECTION': 'close', 'ACCEPT_ENCODING': 'identity',
                                                               'USER_AGENT': 'Python-urllib/3.4',
                                                               'HOST': '127.0.0.1:8000'}, 'COOKIE': [], 'GET': []})
        self.assertFalse(post['msg'] == "")
        self.assertEqual(post['errmsg'], "")


if __name__ == '__main__':
    unittest.main()
