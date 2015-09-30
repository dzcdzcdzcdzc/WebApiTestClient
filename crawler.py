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

    # get请求
    # @param get_url get请求地址
    # @param timeout 超时时间
    def get(self, get_url, header, timeout=120):
        data = {}
        try:
            data['error'] = 0
            req = urllib.request.Request(self.quote_url(get_url))
            if header != {}:
                for k, v in header.items():
                    req.add_header(k.lower(), v)
            urlopen = urllib.request.urlopen(req, timeout=timeout)
            # 发送包的头文件
            data['info'] = "发送包的头文件：\n"
            for k, v in req.header_items():
                data['info'] += k + ": " + v + "\n"
            data['info'] += "\n"
            # 接收包的头文件
            data['info'] += "接收包的头文件：\n" + str(urlopen.info()) + "\n"
            data['read'] = urlopen.read()
            data['read'], data['msg'], data['errmsg'] = self.decode_json(data['read'])
        except (urllib.error.URLError, ValueError) as e:
            data['error'] = 1
            data['errmsg'] = e
        #except Exception as e:
        #    data['error'] = 2
        #    data['errmsg'] = e
        return data

    def post(self, post_url, post, header, timeout=120):
        data = {}
        try:
            data['error'] = 0
            post = urllib.parse.urlencode(post)
            post = post.encode('utf-8')
            req = urllib.request.Request(self.quote_url(post_url), data=post, method='POST')
            if header == {}:
                urlopen = urllib.request.urlopen(req, timeout=timeout)
            else:
                for k, v in header.items():
                    req.add_header(k.lower(), v)
                urlopen = urllib.request.urlopen(req, timeout=timeout)
            # 发送包的头文件
            data['info'] = "发送包的头文件：\n"
            for k, v in req.header_items():
                data['info'] += k + ": " + v + "\n"
            data['info'] += "\n"
            # 接收包的头文件
            data['info'] += "接收包的头文件：\n" + str(urlopen.info()) + "\n"
            data['read'] = urlopen.read()
            data['read'], data['msg'], data['errmsg'] = self.decode_json(data['read'])
        except (urllib.error.URLError, ValueError) as e:
            data['error'] = 1
            data['errmsg'] = e
        except Exception as e:
            data['error'] = 2
            data['errmsg'] = e
        return data

    # 转换url中的中文字符
    # @param quote_url 转换字符
    def quote_url(self, quote_url):
        # 保护url中的://不被转换
        quote_url = quote_url.split("//", 1)
        if len(quote_url) == 2:
            quote_url[1] = urllib.request.quote(quote_url[1], self.safe)
        else:
            raise ValueError
        quote_url = '//'.join(quote_url)
        return quote_url

    # Sample Text去除网页中的开头的bom和结尾的回车空格
    # @param word 过滤文字
    def filter(self, word, msg):
        r = re.compile(r"^\s+")
        if re.search(r, word) is not None:
            msg += "网页开头含有非空字符\n"
            word = re.sub(r, "", word)
        r = re.compile(r"$\s+")
        if re.search(r, word) is not None:
            msg += "网页末尾有非空字符\n"
            word = re.sub(r, "", word)
        return [word, msg]

    # 解析json字符串
    def decode_json(self, read):
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
            msg += "网页编码转换" + self.code + "时失败，输出源编码"
            errmsg = e
        except ValueError as e:
            msg += "解析json出错，输出原内容。"
            errmsg = e
        except Exception as e:
            msg += "解析原网页，出现非致命错误："
            errmsg = e
        return [read, msg, str(errmsg)]


if __name__ == '__main__':
    Test = Test()
    url = "http://localhost/work/phptext/error.php?id=1&name=的"
    post_data = {'spam': 1, 'eggs': 2, 'bacon': 0}
    a = Test.post(url, post_data, {})
    if a['error'] == 0:
        print(a['read'] + "\n", "msg" + a['msg'] + "\n", "err" + a['errmsg'] + "\n")
    else:
        print(a['errmsg'])
