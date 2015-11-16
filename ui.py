from tkinter import *
from tkinter.ttk import *

__author__ = 'zhichen.dai'


class TestUI(object):
    # _mode_value 发送模式
    _mode_value = 'GET'
    # _key_entry 参数框架的key值文本框对象
    # _value_entry 参数框架的value值文本框对象
    # _value_del_button 参数框架的删除按钮，为了简化“判断删除按钮是否应该禁用”
    # mode_row 打包上面对象，传参使用
    _key_entry = []
    _value_entry = []
    _value_del_button = []
    mode_row = (_key_entry, _value_entry, _value_del_button)
    # _header_check 发送header复选框
    _header_check = 0
    # _key_entry HEADER框架的key值文本框对象
    # _value_entry HEADER框架的value值文本框对象
    # _value_del_button HEADER框架的删除按钮
    # header_row 打包上面对象，传参使用
    _header_key = []
    _header_value = []
    _header_del_button = []
    header_row = (_header_key, _header_value, _header_del_button)
    # url文本框对象
    _url_entry = object
    # 提交按钮对象
    _submit_button = object
    # 下方左边文本框对象
    _header_text = object
    # 下方右边文本框对象
    _body_text = object

    def __init__(self, master=None):
        self.root = master
        # 生成控制框架
        self.console_frame()
        # 生成结果框架
        result_frame = Frame()
        self._header_text = Text(result_frame, state="normal", width=1)
        self._body_text = Text(result_frame, state="normal", width=1)
        result_frame.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self._header_text.pack(side=LEFT, expand=YES, fill=BOTH)
        self._body_text.pack(side=RIGHT, expand=YES, fill=BOTH)
        # 禁止文本框输入
        self._header_text.bind("<KeyPress>", lambda e: "break")
        self._body_text.bind("<KeyPress>", lambda e: "break")

    def console_frame(self):
        """
        模式和url行
        :return None:
        """
        url_frame = Frame(self.root)
        mode_label = Label(url_frame, text='发送方式：')
        mode = Combobox(url_frame, width=5, values=["GET", "POST"], state="readonly")
        mode.set("GET")
        url_label = Label(url_frame, text='请求地址：')
        self._url_entry = Entry(url_frame)
        url_frame.pack(side=TOP, fill=X)
        mode_label.pack(side=LEFT)
        mode.pack(side=LEFT)
        url_label.pack(side=LEFT)
        self._url_entry.pack(side=RIGHT, expand=YES, fill=X)
        # POST参数行
        value_frame = Frame(self.root)
        value_frame.pack(side=TOP, fill=X)
        # HEADER参数行
        header_frame = Frame(self.root)
        header_frame.pack(side=TOP, fill=X)
        # 提交按钮行
        submit_frame = Frame(self.root)
        header_check = IntVar()
        header = Checkbutton(submit_frame, variable=header_check, text="包含HEADER", width=15,
                             command=(lambda: self.header_change(header_check.get(), header_frame)))
        submit_frame.pack(side=TOP, fill=X)
        header.pack(side=LEFT)
        self._submit_button = Button(submit_frame, text="提交", width=10, command=(lambda: self.submit()))
        self._submit_button.pack(side=RIGHT)
        # 动作
        mode.bind('<<ComboboxSelected>>', (lambda event: self.mode_change(mode.get(), value_frame)))

    def mode_change(self, mode_value, value_frame):
        """
        修改模式触发
        :param mode_value 下拉框的值:
        :param value_frame 之后变动的frame对象:
        :return None:
        """
        self._mode_value = mode_value
        if self._mode_value == 'GET':
            self.del_all_value(value_frame, self.mode_row)
        elif self._mode_value == 'POST':
            if not value_frame.children:
                self.add_all_value(value_frame, "POST:", self.mode_row)
        else:
            raise ValueError

    def header_change(self, header_check, header_frame):
        """
        勾选HEADER触发
        :param header_check 复选框的值:
        :param header_frame 之后变动的frame对象:
        :return None:
        """
        self._header_check = header_check
        if self._header_check == 0:
            self.del_all_value(header_frame, self.header_row)
        elif self._header_check == 1:
            if not header_frame.children:
                self.add_all_value(header_frame, "HEADER:", self.header_row)

    def add_value(self, value_frame, row):
        """
        增加一行输入框
        :param value_frame 增加一行的value_frame对象:
        :param row 键、值文本框和删除按钮对象的元组:
        :return None:
        """
        key_entry, value_entry, delete_button = row
        row_value = Frame(value_frame)
        row_value.pack(side=TOP, fill=X)
        key_label = Label(row_value, text="key:")
        key_label.pack(side=LEFT)
        key = Entry(row_value)
        key.pack(side=LEFT, expand=YES, fill=X)
        value_label = Label(row_value, text="value:")
        value_label.pack(side=LEFT)
        value = Entry(row_value)
        value.pack(side=LEFT, expand=YES, fill=X)
        del_button = Button(row_value, text="删除", width=5, state="disabled")
        del_button.pack(side=RIGHT)
        key_entry.append(key)
        value_entry.append(value)
        delete_button.append(del_button)
        del_button.bind('<ButtonRelease>',
                        (lambda event: self.del_value(value_frame, event.widget,
                                                      (key_entry, value_entry, delete_button))))
        self.button_disable(value_frame, (key_entry, value_entry, delete_button))

    def del_value(self, value_frame, button, row):
        """
        删除一行输入框
        :param value_frame  删除一行的value_frame对象:
        :param button 触发此方法的删除按钮对象:
        :param row 键、值文本框和删除按钮对象的元组:
        :return None:
        """
        key_entry, value_entry, delete_button = row
        for widget in button.master.children.values():
            widget in key_entry and key_entry.remove(widget)
            widget in value_entry and value_entry.remove(widget)
            widget in delete_button and delete_button.remove(widget)
        button.master.destroy()
        self.button_disable(value_frame, (key_entry, value_entry, delete_button))

    def add_all_value(self, frame, text, row):
        """
        增加一行添加按钮行
        :param frame 增加一行的frame:
        :param text 显示的说明文字:
        :param row 键、值文本框和删除按钮对象的元组:
        :return None:
        """
        row_value = Frame(frame)
        row_value.pack(side=TOP, fill=X)
        post_label = Label(row_value, text=text)
        post_label.pack(side=LEFT)
        add_button = Button(row_value, text="添加", width=5, command=(lambda: self.add_value(frame, row)))
        add_button.pack(side=RIGHT)
        self.add_value(frame, row)

    @staticmethod
    def del_all_value(frame, row):
        """
        删除一整块输入框
        :param frame 删除所有输入框的frame:
        :param row 要清除键、值文本框和删除按钮对象的元组:
        :return None:
        """
        for v in row:
            v.clear()
        while 1:
            if frame.children:
                frame.children.popitem()[1].destroy()
            else:
                break
        frame.configure(height=1)

    def button_disable(self, value_frame, row):
        """
        判断删除按钮是否应该禁用
        :param value_frame 一群删除按钮所在的frame的对象:
        :param row 键、值文本框和删除按钮对象的元组:
        :return None:
        """
        key_entry, value_entry, delete_button = row
        if len(delete_button) > 1:
            for button in delete_button:
                button.configure(state="normal")
                button.bind('<ButtonRelease>',
                            (lambda event: self.del_value(value_frame, event.widget,
                                                          (key_entry, value_entry, delete_button))))
        else:
            delete_button[0].configure(state="disabled")
            # 如果不解绑的话，就算禁用也是可以点击。使用按钮的command参数无法返回是哪个按钮点击的。
            delete_button[0].unbind('<ButtonRelease>')

    def submit(self):
        """
        点击提交调用，仅供改写使用
        :return:
        """
        print([self._mode_value, len(self._key_entry), len(self._value_entry), len(self._value_del_button),
               self._header_check, len(self._header_key), len(self._header_value), len(self._header_del_button)])


if __name__ == '__main__':
    root = Tk()
    root.title("接口测试工具")
    TestUI(master=root)
    root.maxsize(1000, 800)
    root.minsize(450, 240)
    root.resizable(True, True)
    root.mainloop()
