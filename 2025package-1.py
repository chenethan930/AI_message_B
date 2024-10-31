import requests
import json
# from opencc import OpenCC
import streamlit as st
# cc = OpenCC('s2t')

headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets["api_key"]}"
        }

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True
array = []

st.write("## 新年賀詞生產器-B")
name = st.text_input("輸入您的名字")

if name:

    if not is_all_chinese(name):
        
        prompt = f"""請將以下英文名字翻為相似的中文（如：金jenny變成「金珍妮」）：{name}"""

        payload = {
            "model": "gpt-4o-mini",
            "response_format":  { 
                "type": "json_schema",
                "json_schema": {
                        "name": "clothing_json",
                        "strict": True,
                        "schema":{
                                "type": "object",
                                "properties": {
                                "中文翻譯": {
                                    "type": "string"
                                }
                                },
                                "required": [
                                "中文翻譯"
                                ],
                                "additionalProperties": False
                            }
                    }
            },
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": prompt
                    },
                ]
                }
            ],
            }


        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        message_sub1 = response.json()
        answer = json.loads(message_sub1['choices'][0]['message']['content'])

        name = answer["中文翻譯"]
      

    for i in range(len(name)):
        prompt = f"""請給我與「{name[i]}」同音的三個字，並分別放於"字1"，"字2","字3"中。"""

        payload = {
            "model": "gpt-4o-mini",
            "response_format":  { 
                "type": "json_schema",
                "json_schema": {
                        "name": "clothing_json",
                        "strict": True,
                        "schema":{
                                "type": "object",
                                "properties": {
                                "字1": {
                                    "type": "string"
                                },
                                "字2": {
                                    "type": "string"
                                },
                                "字3": {
                                    "type": "string"
                                }
                                },
                                "required": [
                                "字1",
                                "字2",
                                "字3"
                                ],
                                "additionalProperties": False
                            }
                    }
            },
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": prompt
                    },
                ]
                }
            ],
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        message_sub1 = response.json()
        answer = json.loads(message_sub1['choices'][0]['message']['content'])

        array.append(name[i])
        # array.append(cc.convert(answer["字1"]))
        # array.append(cc.convert(answer["字2"]))
        # array.append(cc.convert(answer["字3"]))
        array.append((answer["字1"]))
        array.append((answer["字2"]))
        array.append((answer["字3"]))



    print(array)

    # prompt = f"""你是一個新年賀詞產生專家，接下來請產出一個新年四字賀詞，且該四字賀詞需為新年會使用的吉祥話，並須與新年祝賀相關。注意，此四字賀詞要能出現以下其中一字：{array}，且一定要是四字新春賀詞。（註：請勿在賀詞中提及動物，蛇除外）請將四字賀詞放於"四字賀詞"中，再把你選用的字放在"選字"中。注意，請避免出現「新年快樂」一詞。
    # 倘若上列沒有適合使用的詞放在新年賀詞中，請直接回傳一個新年賀詞，並在"選字"中標示「無」。"""
    prompt = f"""你是一個新年賀詞產生專家，接下來請產出一個新年四字賀詞，且該四字賀詞需為新年會使用的吉祥話，並須與新年祝賀相關。注意，此四字賀詞要能出現以下其中一字：{array}，且一定要是四字新春賀詞。（註：請勿在賀詞中提及動物，蛇除外）請將四字賀詞放於"四字賀詞"中，再把你選用的字放在"選字"中。注意，請避免出現「新年快樂」一詞。
    倘若上列沒有適合使用的詞放在新年賀詞中，請根據該列表中某個字所引伸的意思，生成一個四字新年賀詞（如：「漲」代表上升，因此生成代表上升的賀詞「蒸蒸日上」，並把你選用的字放在"選字"中，並將你選用此字的解釋放於「解釋」中）。"""
    # prompt = f"""你是一個新年賀詞產生專家，接下來會給你一個人的名字，請發揮你說文解字及諧音的知識（注意，請盡可能取與名字的諧音相關的賀詞，若沒有，再使用說文解字），產出一個屬於該名字的新年四字賀詞，且該四字賀詞需為新年會使用的吉祥話，並須與新年祝賀相關。。（註：請勿在賀詞中提及動物，蛇除外）請將四字賀詞放於"四字賀詞"中，並將你選用該賀詞與名字的關聯原因放於「解釋」中，以下為使用者的名字：{name}"""
    payload = {
        "temperature": 0.9,
        "model": "gpt-4o-mini",
        "response_format":  { 
            "type": "json_schema",
            "json_schema": {
                    "name": "clothing_json",
                    "strict": True,
                    "schema":{
                            "type": "object",
                            "properties": {
                                "四字賀詞": {
                                    "type": "string"
                                },
                                "選字": {
                                    "type": "string"
                                },
                                 "解釋": {
                                    "type": "string"
                                }
                            },
                            "required": [
                            "四字賀詞",
                            "選字",
                            "解釋"
                            ],
                            "additionalProperties": False
                        }
                }
        },
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
            ]
            }
        ],
    }


    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    message_sub1 = response.json()
    answer = json.loads(message_sub1['choices'][0]['message']['content'])

    st.caption("生成結果")
    st.write(answer["四字賀詞"])
    print(answer["四字賀詞"])
    print(answer["選字"])
    print(answer["解釋"])
