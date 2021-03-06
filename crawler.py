import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import re


class Test(object):
    # 不将网址之中的以下字符转换，至少要有 ?=&
    safe = '`~!@#$%^&&*()-=_+[][\{}|:";\'<>?,./'
    # 网页编码
    code = 'utf-8'

    def get(self, get_url, header):
        """
        get请求
        :param get_url: get请求地址
        :param header: header头
        :return:获得错误编号和信息
        """
        data = {'error': 0, 'msg': '', 'errmsg': '', 'read': '', 'info': ''}
        try:
            req = urllib.request.Request(self.quote_url(get_url))
            for k, v in header.items():
                req.add_header(k.lower(), v)
            dict(data, **self.request(data, req))
        except (urllib.error.URLError, ValueError) as e:
            data['error'] = 1
            data['errmsg'] = str(e)
        except http.client.BadStatusLine as e:
            data['error'] = 2
            data['read'] = '' if str(e) == "''" else str(e)
        except http.client.InvalidURL as e:
            data['error'] = 3
            data['errmsg'] = str(e)
        except Exception as e:
            data['error'] = 99
            data['errmsg'] = str(e)
        return data

    def post(self, post_url, post, header):
        """
        post请求
        :param post_url: post请求地址
        :param post: post内容
        :param header: header头
        :return:获得错误编号和信息
        """
        data = {'error': 0, 'msg': '', 'errmsg': '', 'read': '', 'info': ''}
        try:
            post = urllib.parse.urlencode(post)
            post = post.encode('utf-8')
            req = urllib.request.Request(self.quote_url(post_url), data=post, method='POST')
            for k, v in header.items():
                req.add_header(k.lower(), v)
            dict(data, **self.request(data, req))
        except (urllib.error.URLError, ValueError) as e:
            data['error'] = 1
            data['errmsg'] = str(e)
        except http.client.BadStatusLine as e:
            data['error'] = 2
            data['read'] = '' if str(e) == "''" else str(e)
        except http.client.InvalidURL as e:
            data['error'] = 3
            data['read'] = str(e)
        except Exception as e:
            data['error'] = 99
            data['errmsg'] = str(e)
        return data

    def request(self, data, req):
        """
        发送请求
        :param data: 信息内容
        :param req: 请求类型、内容
        :return:获得错误编号和信息
        """
        with urllib.request.urlopen(req) as urlopen:
            # 发送包的头文件
            data['info'] = "发送包的头文件：\n"
            for k, v in req.header_items():
                data['info'] += k + ": " + v + "\n"
            data['info'] += "\n"
            # 接收包的头文件
            data['info'] += "接收包的头文件：\n" + str(urlopen.info()) + "\n"
            data['read'] = urlopen.read()
            data['read'], data['msg'], data['errmsg'] = self.decode_json(data['read'])
        return data

    def quote_url(self, quote_url):
        """
        转换url中的中文字符
        :param quote_url: 要转换字符
        :return:转换后的字符
        """
        # 保护url中的://不被转换
        quote_url = quote_url.split("//", 1)
        if len(quote_url) == 2:
            quote_url[1] = urllib.request.quote(quote_url[1], self.safe)
        else:
            raise ValueError
        quote_url = '//'.join(quote_url)
        return quote_url

    # 去除网页中的开头的bom和结尾的回车空格
    # @param word 过滤文字
    @staticmethod
    def filter(word, msg):
        """
        去除网页中的开头的bom和结尾的回车空格
        :param word: 过滤文字
        :param msg: 需要附加的信息
        :return:过滤后的文字和附加完成的信息
        """
        r = re.compile(r"^\s+")
        if re.search(r, word) is not None:
            msg += "网页开头含有非空字符\n"
            word = re.sub(r, "", word)
        r = re.compile(r"$\s+")
        if re.search(r, word) is not None:
            msg += "网页末尾有非空字符\n"
            word = re.sub(r, "", word)
        return word, msg

    def decode_json(self, read):
        """
        解析json字符串
        :param read: 需要解析json的字符串
        :return:解析后的字符串和其他信息
        """
        msg = ""
        errmsg = ""
        try:
            # 去除bom
            if read.find(b'\xef\xbb\xbf') == 0:
                read = read[3:]
                msg += "注意网页开头含有bom\n"
            # 精确模式转换，转换出错提出UnicodeDecodeError错误
            temp = read.decode(self.code)
            temp, msg = self.filter(temp, msg)
            # 解析json，转换非json提出ValueError错误
            read = json.loads(temp)
            # 转换成json，能解析一定能转换
            read = json.dumps(read, ensure_ascii=False, indent=4)
        except UnicodeDecodeError as e:
            msg += "网页编码转换" + self.code + "时失败，输出源编码\n"
            errmsg = e
        except ValueError as e:
            msg += "解析json出错，输出原内容。\n"
            errmsg = e
        except Exception as e:
            msg += "解析原网页，出现非致命错误：\n"
            errmsg = e
        return read, msg, str(errmsg)
