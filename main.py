from tkinter import *
import platform
import ui
import crawler

__author__ = 'zhichen.dai'


class CrawlerUI(ui.TestUI):
    def __init__(self, master=None):
        super(CrawlerUI, self).__init__()
        self.root = master
        self.test = crawler.Test()

    def submit(self):
        url = self._url_entry.get()
        # 地址开头没有http:自动加上http://
        if url.find("http"):
            self._url_entry.insert(0, "http://")
            url = "http://" + url
        if self._mode_value == 'GET':
            # 读取参数发送
            header = self.get_dict(self._header_key, self._header_value)
            dict_result = self.test.get(url, header)
        elif self._mode_value == 'POST':
            # 读取参数发送
            post = self.get_dict(self._key_entry, self._value_entry)
            header = self.get_dict(self._header_key, self._header_value)
            dict_result = self.test.post(url, post, header)
        else:
            raise ValueError
        self.result(dict_result)

    def result(self, dict_result):
        """
        写入结果到UI
        :param dict_result 需要写入的信息:
        :return:
        """
        self.clear_text()
        if dict_result['error'] == 0:
            pass
        elif dict_result['error'] == 1:
            self._header_text.insert(END, "致命错误：连接出错\n"
                                          "1.检查输入的地址是否正确\n"
                                          "2.检查输入的POST是否正确\n"
                                          "2.HEADER中不允许有中文字符\n")
        elif dict_result['error'] == 2:
            self._header_text.insert(END, "致命错误：解析出错\n"
                                          "1.无法解析返回的状态\n")
        elif dict_result['error'] == 99:
            self._header_text.insert(END, "致命错误：程序出错\n")
        self.insert_text(dict_result)

    @staticmethod
    def get_dict(key, value):
        """
        传入key和value的text对象获取字典值
        :param key key值对象的list:
        :param value value值对象的list:
        :return key和value匹配的字典:
        """
        return dict(zip(map(lambda k: k.get(), key), map(lambda k: k.get(), value)))

    def clear_text(self):
        """
        清除文本框内容
        :return None:
        """
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)

    def insert_text(self, info):
        """
        插入文本框内容
        :param info 写入文本框的内容:
        :return None:
        """
        self._header_text.insert(END, info['info'])
        self._header_text.insert(END, info['msg'] + "\n")
        self._header_text.insert(END, info['errmsg'] + "\n")
        self._body_text.insert(END, info['read'])


if __name__ == '__main__':
    root = Tk()
    root.title("接口测试工具")
    CrawlerUI(master=root)
    root.minsize(450, 240)
    sys = platform.system()
    if sys == "Windows":
        root.wm_state('zoomed')
    root.mainloop()
