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
            get = self.test.get(url, header)
            self.text_state(self.get_result, get)
        elif self._mode_value == 'POST':
            # 读取参数发送
            post = self.get_dict(self._key_entry, self._value_entry)
            header = self.get_dict(self._header_key, self._header_value)
            post = self.test.post(url, post, header)
            self.text_state(self.post_result, post)

    # 模拟成修饰符
    def text_state(self, fun, mode):
        self._header_text.configure(state="normal")
        self._body_text.configure(state="normal")
        fun(mode)
        self._header_text.configure(state="disabled")
        self._body_text.configure(state="disabled")

    # 写入get结果到UI
    def get_result(self, get):
        self.clear_text()
        if get['error'] == 0:
            self.insert_text(get)
        elif get['error'] == 1:
            self._header_text.insert(END, "致命错误：连接出错\n"
                                          "1.检查输入的地址是否正确\n"
                                          "2.HEADER中不允许有中文字符\n")
            self._header_text.insert(END, get['errmsg'])
        elif get['error'] == 2:
            self._header_text.insert(END, "致命错误：程序出错\n")
            self._header_text.insert(END, get['errmsg'])

    # 写入post结果到UI
    def post_result(self, post):
        self.clear_text()
        if post['error'] == 0:
            self.insert_text(post)
        elif post['error'] == 1:
            self._header_text.insert(END, "致命错误：连接出错\n"
                                          "1.检查输入的地址是否正确\n"
                                          "2.检查输入的POST是否正确\n"
                                          "3.HEADER中不允许有中文字符\n")
            self._header_text.insert(END, post['errmsg'])
        elif post['error'] == 2:
            self._header_text.insert(END, "致命错误：程序出错\n")
            self._header_text.insert(END, post['errmsg'])

    # 传入key和value的text对象获取字典值
    @staticmethod
    def get_dict(key, value):
        return dict(zip(map(lambda k: k.get(), key), map(lambda k: k.get(), value)))

    # 清除文本框内容
    def clear_text(self):
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)

    # 插入文本框内容
    def insert_text(self, info):
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
