from openai import OpenAI
from pathlib import Path
import base64
import time
import json
from tqdm import tqdm
client = OpenAI(api_key="0", base_url="http://0.0.0.0:9000/v1")


name_list=[
"boxlm_m3_dp_005",
]

for name in name_list:
    total_time = 0

    model_name = "Qwen3-8B"
    json_path = f'data/{name}.json'
    with open(json_path,'r') as f:
        data = json.load(f)



    res=[]
    import os
    file_path = f"result/{name}_{model_name}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            res = json.load(f)
    else:
        res = []
    data=data[len(res):]
    for item in tqdm(data):
        start_time = time.time()
        prompt = item['instruction']+'\n'+item['input']
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ]

        result = client.chat.completions.create(
            messages=messages,
            model=model_name
        )

        item['pred']=result.choices[0].message.content
        res.append(item)
        end_time = time.time()
        total_time+=(end_time - start_time)
        with open(f"result/{name}_{model_name}.json", 'w') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

