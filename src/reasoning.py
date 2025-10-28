
from huggingface_hub import InferenceClient
import os
from system_config import SERVICE
token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

client_h = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=token)

from openai import OpenAI 
client = OpenAI() 
def ask_reasoning(question: str, temperature:float, max_tokens:int) -> str: 
    if SERVICE=='hugging':
        response = client_h.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": "You are a reasoning engine that provides detailed explanations."},
            {"role": "user", "content": question},
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
        return response.choices[0].message["content"]
    else:
        response = client.chat.completions.create( model="gpt-4.1-mini", 
                                                messages=[ {"role": "system", "content": "You are a reasoning engine that provides detailed explanations."}, 
                                                            {"role": "user", "content": question} ],
                                                              max_completion_tokens=max_tokens,
                                                                ) 
        return response.choices[0].message.content

