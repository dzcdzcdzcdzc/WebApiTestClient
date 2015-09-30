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
            url = self._url_entry.get()
            header = dict(zip(map(lambda k: k.get(), self._header_key), map(lambda k: k.get(), self._header_value)))
            get = self.test.get(url, header)
            self._header_text.delete("1.0", END)
            self._body_text.delete("1.0", END)
            if get['error'] == 0:
                self._header_text.insert(END, get['info'])
                self._header_text.insert(END, get['msg'] + "\n")
                self._header_text.insert(END, get['errmsg'] + "\n")
                self._body_text.insert(END, get['read'])
            if get['error'] == 1:
                self._header_text.insert(END, "致命错误：连接出错\n"
                                              "1.检查是否是类似http://开头\n"
                                              "2.检查输入的地址是否正确\n"
                                              "3.检查输入的HEADER是否正确\n")
                self._header_text.insert(END, get['errmsg'])
            if get['error'] == 2:
                self._header_text.insert(END, "致命错误：程序出错\n")
                self._header_text.insert(END, get['errmsg'])
        if self._mode_value == 'POST':
            url = self._url_entry.get()
            postdata = dict(zip(map(lambda k: k.get(), self._key_entry), map(lambda k: k.get(), self._value_entry)))
            header = dict(zip(map(lambda k: k.get(), self._header_key), map(lambda k: k.get(), self._header_value)))
            post = self.test.post(url, postdata, header)
            self._header_text.delete("1.0", END)
            self._body_text.delete("1.0", END)
            if post['error'] == 0:
                self._header_text.insert(END, post['info'])
                self._header_text.insert(END, post['msg'] + "\n")
                self._header_text.insert(END, post['errmsg'] + "\n")
                self._body_text.insert(END, post['read'])
            if post['error'] == 1:
                self._header_text.insert(END, "致命错误：连接出错\n"
                                              "1.检查是否是类似http://开头\n"
                                              "2.检查输入的地址是否正确\n"
                                              "3.检查输入的POST是否正确\n"
                                              "4.HEADER中不允许有中文字符\n")
                self._header_text.insert(END, post['errmsg'])
            if post['error'] == 2:
                self._header_text.insert(END, "致命错误：程序出错\n")
                self._header_text.insert(END, post['errmsg'])


if __name__ == '__main__':
    root = Tk()
    root.title("接口测试工具")
    CrawlerUI(master=root)
    root.minsize(450, 240)
    root.wm_state('zoomed')
    root.mainloop()
