import json
import gradio as gr
import requests
import os
import time

URL = "http://127.0.0.1:8188/prompt"
OUTPUT_DIR = "D:/ComfyUI/ComfyUI_windows_portable/ComfyUI/output"
def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)


def generate_image(prompt_text):   
    with open("workflow_api.json", "r") as file_json:
        prompt = json.load(file_json)
        prompt["4"]["inputs"]["text"] = f"digital artwork of a {prompt_text}"
    
    previous_image = get_latest_image(OUTPUT_DIR)
    
    start_queue(prompt)
    
    while True:
        latest_image  = get_latest_image(OUTPUT_DIR)
        if latest_image != previous_image:
            return latest_image
        
        time.sleep(1)
        
demo = gr.Interface(fn=generate_image, inputs=["text"], outputs=["image"])

demo.launch(share=True)
