# import json 
# import uuid
# import urllib.request
# import urllib.parse
# import websocket
# from PIL import Image
# import io

# server_address = "127.0.0.1:8188"

# with open('workflow_api.json', encoding='utf-8') as f:
#     prompt_text = f.read()
# prompt_save = json.loads(prompt_text)

# client_id = str(uuid.uuid4())
# print("client_id: " + client_id)

# def queue_prompt(prompt):
#     p = {"prompt": prompt, "client_id": client_id}
#     data = json.dumps(p).encode('utf-8')
#     req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
#     return json.loads(urllib.request.urlopen(req).read())

# def get_image(filename, subfolder, folder_type):
#     data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
#     url_values = urllib.parse.urlencode(data)
#     with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
#         return response.read()

# def get_history(prompt_id):
#     with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
#         return json.loads(response.read())

# def get_images(ws, prompt):
#     prompt_id = queue_prompt(prompt)['prompt_id']
#     output_images = {}
#     try:
#         while True:
#             try:
#                 out = ws.recv()
#             except TimeoutError:
#                 print("Timeout occurred, no data received from the server.")
#                 return []
#             if isinstance(out, str):
#                 message = json.loads(out)
#                 if message['type'] == 'executing':
#                     data = message['data']
#                     if data['node'] is None and data['prompt_id'] == prompt_id:
#                         break
#             else:
#                 continue

#         history = get_history(prompt_id)[prompt_id]
#         for o in history['outputs']:
#             for node_id in history['outputs']:
#                 node_output = history['outputs'][node_id]
#                 if 'images' in node_output:
#                     images_output = []
#                     for image in node_output['images']:
#                         image_data = get_image(image['filename'], image['subfolder'], image['type'])
#                         images_output.append(image_data)
#                     output_images[node_id] = images_output

#     finally:
#         ws.close()

#     return output_images

# prompt = prompt_save 
# prompt["4"]["inputs"]["text"] = "a snake "
# prompt["6"]["inputs"]["seed"] = 777777777

# ws = websocket.WebSocket()
# ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
# ws.settimeout(120)
# images = get_images(ws, prompt)

# for node_id in images:
#     for image_data in images[node_id]:
#         image = Image.open(io.BytesIO(image_data))
#         image.show()
#         image.save(f"Output - 777777 - {node_id}.png")
