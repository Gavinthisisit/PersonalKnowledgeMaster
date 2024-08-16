#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) <T_COPYRIGHT_YEAR> Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
# @author: gaochenxi (gaochenxi@baidu.com)
# @date: 2024年06月03日 星期一 19时46分34秒
# @file: conversation.py
# @desc:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
File: conversation.py
Author: work(work@baidu.com)
Date: 2024/05/21 15:25:44
"""
import os
import sys
import appbuilder
import logging
import time
import json
from typing import List

logging.basicConfig(filename='example.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

####配置密钥
os.environ["APPBUILDER_TOKEN"] = 'bce-v3/ALTAK-z7WdbEWUR242VCYC1o1IP/8b5619d99e8a458f0da94c3c75895efdbbaa4bf6'

# 配置密钥与应用ID
intent_app_id = "6aee035e-2689-4040-a02b-8785a392b292"
response_app_id = "2bc750b7-3d34-4cca-8f67-c7c7b26a1c20"

 
def deal_intent_response(intent_str):
    # print(intent_str)
    intent_str.replace("\n", "")
    # raw_intent_str = intent_str
    index = intent_str.find('{')
    intent_str = intent_str[index:]
    index = intent_str.rfind('}')
    intent_str = intent_str[:index + 1]
    intent_str = intent_str.replace("，", ",")
    intent_str = intent_str.replace("：", ":")
    # print("-------", intent_str)
    try:
        intent_str = intent_str.strip()
        intent_obj = json.loads(intent_str)
        slots_obj = intent_obj["slots"]
        return intent_str, intent_obj, slots_obj
    except Exception as e:
        print(e)
        pass
    return intent_str.strip(), {"intent": "chat", "slots": {}}, {}


def gen_prompt(session_list):
    if len(session_list) == 0:
        return ""
    retval = "##历史session\n"
    for se in session_list:
        retval += "User:" + se["query"] + "\n"
        retval += "Assistant:" + se["answer"] + "\n"
    retval += "##当前请求"
    return retval


class Session:
    def __init__(self):
        self.session_cnt = 0
        self.session_list = []

    def write(self, query, answer):
        tmp_map = {"query": query, "answer": answer, "time": time.time()}
        self.session_list.append(tmp_map)
        self.session_cnt += 1
        print(self.session_list)

    def get(self):
        print(self.session_cnt)
        print(self.session_list)
        se_list = []
        now_time = time.time()
        index = self.session_cnt - 1
        cnt = 0
        while index >= 0 and cnt < 3:
            session_item = self.session_list[index]
            if now_time - session_item["time"] < 60:
                # 一分钟以内的计入session
                se_list.append(session_item)
                index -= 1
            else:
                # 因为倒序处理，所以遇到第一个超时的直接break，因为前面的肯定超时
                break
            cnt += 1
        # 清理过期session
        self.session_list = self.session_list[index + 1:]
        self.session_cnt = len(self.session_list)
        return se_list


class Conversation:
    def __init__(self, intent_app_id):
        self.intent_agent = appbuilder.AppBuilderClient(intent_app_id)
        self.intent_conversation = self.intent_agent.create_conversation()

    def generate(self, user_query):
        start_time = time.time()
        intent_msg = self.intent_agent.run(self.intent_conversation, user_query)
        end_time = time.time()
        intent_time = end_time - start_time
        print(intent_msg)
        print("意图模型耗时%d s", intent_time)
        intent_str, intent_obj, slots_obj = deal_intent_response(intent_msg.content.answer)
        print("意图模型的返回：", intent_str)
        return intent_str


def get_user_input():
    try:
        return input()
    except Exception as e:
        print(e)
        return ""


if __name__ == '__main__':
    input_txt = "\n".join(open("../data/pp", 'r').readlines())
    # print(len(input_txt))
    conversation = Conversation(intent_app_id, response_app_id)
    conversation.search_pic(input_txt[:1000])