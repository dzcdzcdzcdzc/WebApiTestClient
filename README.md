# WebApiTestClient

<!-- BADGES/ -->
[![Python Version](https://img.shields.io/badge/python-3.3%2C%203.4%2C%203.5-blue.svg)]
[![Build Status](https://travis-ci.org/dzcdzcdzcdzc/WebApiTestClient.svg?branch=master)](https://travis-ci.org/dzcdzcdzcdzc/WebApiTestClient)
[![Code Climate](https://codeclimate.com/github/dzcdzcdzcdzc/WebApiTestClient/badges/gpa.svg)](https://codeclimate.com/github/dzcdzcdzcdzc/WebApiTestClient)
[![Test Coverage](https://codeclimate.com/github/dzcdzcdzcdzc/WebApiTestClient/badges/coverage.svg)](https://codeclimate.com/github/dzcdzcdzcdzc/WebApiTestClient/coverage)
<!-- /BADGES -->
## 简介
python3编写的web api测试工具。使用官方库，安装完python环境包可以直接使用。

启动时不希望已最大化方式打开，就删除main.py中的

    root.wm_state('zoomed')

使用时将main.py重命名成main.pyw，启动时不会出现console。

## 功能
- 请求
 - [X] get
 - [X] post
 - [X] header
 - [ ] put
 - [ ] delete

## 特点
- 允许输入的url带有中文
- 返回的结果如果是json，格式化输出
- 返回的结果开头出现BOM、结束出现空格和回车时，提出警告

## 未来
- 提交请求时会造成短暂的阻塞，计划使用协程解决。届时或许不再支持python3.3
- 加入更多请求功能

## 许可
The MIT License (MIT) http://opensource.org/licenses/MIT
