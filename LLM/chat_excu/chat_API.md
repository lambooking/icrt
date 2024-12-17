# Chat

## 请求示例
### 非流式调用
#### （一）Python调用示例
```python
import requests
import json
def send_query(user_query):
    full_query = {
        "messages": [{"role": "user", "content": user_query}],
        "stream": False,
        "model": "o",
        "temperature": 0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "top_p": 1.0
    }
    # 定义服务器地址
    ngrok_url = 'http://192.168.8.29:9000' 
    try:
        # 发送POST请求
        response = requests.post(f"{ngrok_url}/v1/chat/completions", 
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(full_query))
        response.raise_for_status()
        print("Raw Response Text:", response.text)
        return response
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求出错: {e}")
        return None
# 示例调用
user_query = "请介绍一下傅利叶公司"  # 替换为你的查询内容
response_data = send_query(user_query)
if response_data:
    print("Response:", response_data)
```
**支持参数说明**

- 支持 messages, temperature,  stream,model, presence_penalty, presence_penalty,top_p **:blush:**
- 暂不支持其他参数
#### (二) curl调用示例
```python
curl -X POST http://192.168.8.29:9000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "messages": [{"role": "user", "content": "拜拜"}],
    "stream": false,
    "model": "o",
    "temperature": 0,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "top_p": 1.0
}'
```
### 流式调用示例
#### （一） python调用示例（即将推出）
```python
waiting for edit....
```
#### （二） curl调用示例 （即将推出）
```python
waiting for edit....
```
#### 请求参数说明
| 参数      | 类型 | 参数      | 说明    |
| ----------- | ----------- |----------- | ----------- |
| model      | string       |	internlm2.5-latest|调用的模型名称|
| messages   | array        |[{"role":"user","content":"你好"}]|对话历史及本次提问目前 role (角色)|
| temperature   | 可选，float        |0.8|	采样温度|
| stream   | 可选，bool        |true|流式输出增量结果，使用 tools 功能时不支持流式|
| top_p   | 可选，float        |1.0|候选 token 的概率下限|
| presence_penalty   | 可选，float       |0.0|用于控制是否要避免完全重复的词出现|
|frequency_penalty|可选，float    |0.0|用于控制频繁词的出现次数，防止生成中同一词反复出现|
#### 相关结构体说明
- message结构说明
  
| 参数      | 类型 | 参数      | 说明    |
| ----------- | ----------- |----------- | ----------- |
|role	|string|	user	|user 表示用户提问，assistant 表示模型回答|
content	|string	|你好	|对话内容，当向模型发送 role 为 tool 的请求时，content 内容为调用相应 function 返回的 json string
