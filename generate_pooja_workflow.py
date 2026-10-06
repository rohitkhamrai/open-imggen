import json

# Node template helper
def make_node(id, type, pos, widgets):
    return {
        "id": id,
        "type": type,
        "pos": pos,
        "size": [210, 100],
        "flags": {},
        "order": id,
        "mode": 0,
        "inputs": [],
        "outputs": [],
        "properties": {},
        "widgets_values": widgets
    }

nodes = [
    make_node(1, 'UnetLoaderGGUF', [50, 50], ['zimageTurboByStable_xmasQ8.gguf']),
    make_node(2, 'DualCLIPLoader', [50, 200], ['clip_l.safetensors', 'clip_g.safetensors', 'sdxl']),
    make_node(3, 'VAELoader', [50, 350], ['sdxl_vae.safetensors']),
    make_node(4, 'EmptyLatentImage', [50, 500], [1024, 1024, 3]),
    make_node(5, 'CLIPTextEncode', [400, 50], ['Beautiful Yajna invitation card, glowing fire, marigold garlands, highly detailed, 8k, pooja decoration, intricate borders']),
    make_node(6, 'CLIPTextEncode', [400, 250], ['ugly, watermark, low quality, bad anatomy']),
    make_node(7, 'KSampler', [800, 50], [12345, 'randomize', 20, 7.0, 'euler', 'normal', 1.0]),
    make_node(8, 'VAEDecode', [1100, 50], []),
    make_node(9, 'SaveImage', [1400, 50], ['DaivBharathi_PoojaCard'])
]

# Configure Inputs
nodes[4]['inputs'] = [{'name': 'clip', 'type': 'CLIP', 'link': 1}]  # Node 5
nodes[5]['inputs'] = [{'name': 'clip', 'type': 'CLIP', 'link': 2}]  # Node 6
nodes[6]['inputs'] = [ # Node 7 KSampler
    {'name': 'model', 'type': 'MODEL', 'link': 3},
    {'name': 'positive', 'type': 'CONDITIONING', 'link': 4},
    {'name': 'negative', 'type': 'CONDITIONING', 'link': 5},
    {'name': 'latent_image', 'type': 'LATENT', 'link': 6}
]
nodes[7]['inputs'] = [ # Node 8 VAEDecode
    {'name': 'samples', 'type': 'LATENT', 'link': 7},
    {'name': 'vae', 'type': 'VAE', 'link': 8}
]
nodes[8]['inputs'] = [{'name': 'images', 'type': 'IMAGE', 'link': 9}] # Node 9 SaveImage

# Configure Outputs
nodes[0]['outputs'] = [{'name': 'MODEL', 'type': 'MODEL', 'links': [3]}]
nodes[1]['outputs'] = [{'name': 'CLIP', 'type': 'CLIP', 'links': [1, 2]}]
nodes[2]['outputs'] = [{'name': 'VAE', 'type': 'VAE', 'links': [8]}]
nodes[3]['outputs'] = [{'name': 'LATENT', 'type': 'LATENT', 'links': [6]}]
nodes[4]['outputs'] = [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [4]}]
nodes[5]['outputs'] = [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [5]}]
nodes[6]['outputs'] = [{'name': 'LATENT', 'type': 'LATENT', 'links': [7]}]
nodes[7]['outputs'] = [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [9]}]

# link structure: [link_id, from_node, from_slot, to_node, to_slot, type]
links = [
    [1, 2, 0, 5, 0, 'CLIP'],
    [2, 2, 0, 6, 0, 'CLIP'],
    [3, 1, 0, 7, 0, 'MODEL'],
    [4, 5, 0, 7, 1, 'CONDITIONING'],
    [5, 6, 0, 7, 2, 'CONDITIONING'],
    [6, 4, 0, 7, 3, 'LATENT'],
    [7, 7, 0, 8, 0, 'LATENT'],
    [8, 3, 0, 8, 1, 'VAE'],
    [9, 8, 0, 9, 0, 'IMAGE']
]

workflow = {
    'last_node_id': 10,
    'last_link_id': 10,
    'nodes': nodes,
    'links': links,
    'groups': [],
    'config': {},
    'extra': {}
}

with open(r'C:\Users\rohit\.gemini\antigravity-ide\brain\75ca5046-c050-4870-bd18-6c550995f008\Pooja_Card_Workflow.json', 'w') as f:
    json.dump(workflow, f, indent=2)
