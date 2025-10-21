
from huggingface_hub import InferenceClient
import os
token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=token)

def ask_reasoning(question: str) -> str:
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": "You are a reasoning engine that provides detailed explanations."},
            {"role": "user", "content": question},
        ],
        max_tokens=512,
    )
    return response.choices[0].message["content"]
"""
from openai import OpenAI 
client = OpenAI() 
def ask_reasoning(question: str) -> str: 
    response = client.chat.completions.create( model="gpt-4", 
                                              messages=[ {"role": "system", "content": "You are a reasoning engine that provides detailed explanations."}, 
                                                        {"role": "user", "content": question} ] ) 
    return response.choices[0].message.content
"""