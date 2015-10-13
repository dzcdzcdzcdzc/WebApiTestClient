from tkinter import *
import ui
import crawler

__author__ = 'zhichen.dai'


class CrawlerUI(ui.TestUI):
    def __init__(self, master=None):
        super(CrawlerUI, self).__init__()
        self.root = master
        self.test = crawler.Test()

    def submit(self):
        if self._mode_value == 'GET':
            # 读取参数发送
            url = self._url_entry.get()
            header = dict(zip(map(lambda k: k.get(), self._header_key), map(lambda k: k.get(), self._header_value)))
            get = self.test.get(url, header)
            self._header_text.configure(state="normal")
            self._body_text.configure(state="normal")
            self.get_result(get)
            self._header_text.configure(state="disabled")
            self._body_text.configure(state="disabled")
        elif self._mode_value == 'POST':
            # 读取参数发送
            url = self._url_entry.get()
            post = dict(zip(map(lambda k: k.get(), self._key_entry), map(lambda k: k.get(), self._value_entry)))
            header = dict(zip(map(lambda k: k.get(), self._header_key), map(lambda k: k.get(), self._header_value)))
            post = self.test.post(url, post, header)
            self._header_text.configure(state="normal")
            self._body_text.configure(state="normal")
            self.post_result(post)
            self._header_text.configure(state="disabled")
            self._body_text.configure(state="disabled")

    # 写入get结果到UI
    def get_result(self, get):
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)
        if get['error'] == 0:
            self._header_text.insert(END, get['info'])
            self._header_text.insert(END, get['msg'] + "\n")
            self._header_text.insert(END, get['errmsg'] + "\n")
            self._body_text.insert(END, get['read'])
        elif get['error'] == 1:
            self._header_text.insert(END, "致命错误：连接出错\n"
                                          "1.检查URL是否是类似http://开头\n"
                                          "2.检查输入的地址是否正确\n"
                                          "3.HEADER中不允许有中文字符\n")
            self._header_text.insert(END, get['errmsg'])
        elif get['error'] == 2:
            self._header_text.insert(END, "致命错误：程序出错\n")
            self._header_text.insert(END, get['errmsg'])

    # 写入post结果到UI
    def post_result(self, post):
        self._header_text.delete("1.0", END)
        self._body_text.delete("1.0", END)
        if post['error'] == 0:
            self._header_text.insert(END, post['info'])
            self._header_text.insert(END, post['msg'] + "\n")
            self._header_text.insert(END, post['errmsg'] + "\n")
            self._body_text.insert(END, post['read'])
        elif post['error'] == 1:
            self._header_text.insert(END, "致命错误：连接出错\n"
                                          "1.检查URL是否是类似http://开头\n"
                                          "2.检查输入的地址是否正确\n"
                                          "3.检查输入的POST是否正确\n"
                                          "4.HEADER中不允许有中文字符\n")
            self._header_text.insert(END, post['errmsg'])
        elif post['error'] == 2:
            self._header_text.insert(END, "致命错误：程序出错\n")
            self._header_text.insert(END, post['errmsg'])


if __name__ == '__main__':
    root = Tk()
    root.title("接口测试工具")
    CrawlerUI(master=root)
    root.minsize(450, 240)
    root.wm_state('zoomed')
    root.mainloop()
