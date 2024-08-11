import json
import os
from time import sleep

import pandas as pd
import requests

API_KEY = "************"
SECRET_KEY = "************"


def get_access_token():
    '''
    获取百度API的access token
    :return: access token
    '''
    url_token = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url_token, params=params)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
    else:
        raise Exception("获取 access token 失败: {} - {}".format(response.status_code, response.text))
    return access_token


def WenXinYiYan(prompt, language):
    '''
    获取百度API的access token
    获取文心一言API的回答
    :param prompt:
    :return:
    '''
    if language == 'en':
        system_prompt = 'Give clear choices and responses, be concise and accurate, do not be ambiguous, and do not need to explain the reasons. Response language: English.'
    else:
        system_prompt = '给出明确选择和回复，简洁准确，不能模棱两可，无需解释原因。回复语言：中文。'

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "top_p": 0.9,
        "penalty_score": 1,
        "system": system_prompt,
        "disable_search": True,
        "enable_citation": False,
        "max_output_tokens": 512
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if '443' in str(response.text):
        while response.status_code != 200:
            response = requests.request("POST", url, headers=headers, data=payload)
            sleep(5)
    response_text = json.loads(response.text)
    # print(response_text["result"])
    return response_text["result"]


# prompt_path 提问文件路径
prompt_path = '../prompt/'
# output_path 输出文件路径
output_path = '../output/WenXinYiYan/'


def read_txt(filename):
    '''
    读取txt文件
    :param filename: 要读取prompt的文件名
    :return: 包含每行内容的字典，值为None
    '''
    with open(prompt_path + filename, 'r', encoding='utf-8') as file:
        data = file.readlines()
    # 创建字典，将每一行作为键，值暂时为None
    result = {line.strip(): None for line in data}

    return result


def write_csv(filename, json_data, column1, column2):
    """
    将JSON数据写入CSV文件，键写入column1列，值写入column2列。
    若文件不存在则创建文件，若列不存在则创建列，列存在则追加写入。

    :param filename: 文件名
    :param json_data: JSON字符串
    :param column1: 键的列名
    :param column2: 值的列名
    """
    # 解析JSON字符串为字典
    data = json.loads(json_data)

    # 创建一个DataFrame，用于存储JSON数据的键和值
    new_df = pd.DataFrame(list(data.items()), columns=[column1, column2])

    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    if file_exists:
        # 读取现有的CSV文件
        df = pd.read_csv(filename)

        # 检查列是否存在，如果不存在则创建
        if column1 not in df.columns:
            df[column1] = None
        if column2 not in df.columns:
            df[column2] = None

        # 追加新数据
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df

    # 写入CSV文件
    df.to_csv(output_path + filename, index=False)


def ask(method, language, llms):
    prompts_file = method + "_prompts_" + language + ".txt"
    output_file = method + "_" + llms + "Answer_" + language + "_3.csv"

    prompts = read_txt(prompts_file)
    print("-------------------下面开始测试prompt---------------------")
    time = 1
    for prompt, answer in prompts.items():
        try:
            prompts[prompt] = WenXinYiYan(prompt, language).replace("\n", "  ")
            print(f"第{time}次: Prompt: {prompt}  Answer: {prompts[prompt]}")
            print("-------------------------------------")
            time += 1
            if time % 150 == 0:
                sleep(15)
        except Exception as e:
            print(e)

    try:
        write_csv(output_file, json.dumps(prompts), 'prompt_' + language, method + '_' + llms + 'Answer_' + language)
        print(f"已经写入{output_file}文件")
    except Exception as e:
        print(e)
        print("写入csv文件失败")


if __name__ == '__main__':
    llms = 'WenXinYiYan'  # WenXinYiYan ZhiPuQingYan
    language = 'zh'  # en

    method = 'method1'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method2'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method3'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method4'  # method1 method2 method3 method4
    ask(method, language, llms)

    language = 'en'
    method = 'method1'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method2'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method3'  # method1 method2 method3 method4
    ask(method, language, llms)

    method = 'method4'  # method1 method2 method3 method4
    ask(method, language, llms)
