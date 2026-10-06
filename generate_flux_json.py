import json

workflow = {
  "last_node_id": 9,
  "last_link_id": 9,
  "nodes": [
    {
      "id": 1,
      "type": "UnetLoaderGGUF",
      "pos": [0, 0],
      "size": [315, 82],
      "flags": {},
      "order": 0,
      "mode": 0,
      "outputs": [{"name": "MODEL", "type": "MODEL", "links": [3], "slot_index": 0}],
      "properties": {"Node name for S&R": "UnetLoaderGGUF"},
      "widgets_values": ["z_image_turbo-Q5_K_S.gguf"]
    },
    {
      "id": 2,
      "type": "DualCLIPLoader",
      "pos": [0, 200],
      "size": [315, 106],
      "flags": {},
      "order": 1,
      "mode": 0,
      "outputs": [{"name": "CLIP", "type": "CLIP", "links": [1, 2], "slot_index": 0}],
      "properties": {"Node name for S&R": "DualCLIPLoader"},
      "widgets_values": ["t5xxl_fp8_e4m3fn.safetensors", "clip_l.safetensors", "flux"]
    },
    {
      "id": 3,
      "type": "VAELoader",
      "pos": [0, 400],
      "size": [315, 58],
      "flags": {},
      "order": 2,
      "mode": 0,
      "outputs": [{"name": "VAE", "type": "VAE", "links": [8], "slot_index": 0}],
      "properties": {"Node name for S&R": "VAELoader"},
      "widgets_values": ["ae.safetensors"]
    },
    {
      "id": 4,
      "type": "EmptyLatentImage",
      "pos": [0, 600],
      "size": [315, 106],
      "flags": {},
      "order": 3,
      "mode": 0,
      "outputs": [{"name": "LATENT", "type": "LATENT", "links": [6], "slot_index": 0}],
      "properties": {"Node name for S&R": "EmptyLatentImage"},
      "widgets_values": [1024, 1024, 3]
    },
    {
      "id": 5,
      "type": "CLIPTextEncode",
      "pos": [400, 0],
      "size": [400, 200],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [{"name": "clip", "type": "CLIP", "link": 1}],
      "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [4], "slot_index": 0}],
      "properties": {"Node name for S&R": "CLIPTextEncode"},
      "widgets_values": ["Beautiful Yajna invitation card, glowing fire, marigold garlands, highly detailed, 8k, pooja decoration, intricate borders"]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [400, 300],
      "size": [400, 200],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [{"name": "clip", "type": "CLIP", "link": 2}],
      "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [5], "slot_index": 0}],
      "properties": {"Node name for S&R": "CLIPTextEncode"},
      "widgets_values": ["ugly, watermark, low quality, text"]
    },
    {
      "id": 7,
      "type": "KSampler",
      "pos": [900, 0],
      "size": [315, 474],
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {"name": "model", "type": "MODEL", "link": 3},
        {"name": "positive", "type": "CONDITIONING", "link": 4},
        {"name": "negative", "type": "CONDITIONING", "link": 5},
        {"name": "latent_image", "type": "LATENT", "link": 6}
      ],
      "outputs": [{"name": "LATENT", "type": "LATENT", "links": [7], "slot_index": 0}],
      "properties": {"Node name for S&R": "KSampler"},
      "widgets_values": [12345, "randomize", 20, 7.0, "euler", "normal", 1.0]
    },
    {
      "id": 8,
      "type": "VAEDecode",
      "pos": [1300, 0],
      "size": [210, 46],
      "flags": {},
      "order": 7,
      "mode": 0,
      "inputs": [
        {"name": "samples", "type": "LATENT", "link": 7},
        {"name": "vae", "type": "VAE", "link": 8}
      ],
      "outputs": [{"name": "IMAGE", "type": "IMAGE", "links": [9], "slot_index": 0}],
      "properties": {"Node name for S&R": "VAEDecode"}
    },
    {
      "id": 9,
      "type": "SaveImage",
      "pos": [1600, 0],
      "size": [315, 270],
      "flags": {},
      "order": 8,
      "mode": 0,
      "inputs": [{"name": "images", "type": "IMAGE", "link": 9}],
      "properties": {},
      "widgets_values": ["DaivBharathi"]
    }
  ],
  "links": [
    [1, 2, 0, 5, 0, "CLIP"],
    [2, 2, 0, 6, 0, "CLIP"],
    [3, 1, 0, 7, 0, "MODEL"],
    [4, 5, 0, 7, 1, "CONDITIONING"],
    [5, 6, 0, 7, 2, "CONDITIONING"],
    [6, 4, 0, 7, 3, "LATENT"],
    [7, 7, 0, 8, 0, "LATENT"],
    [8, 3, 0, 8, 1, "VAE"],
    [9, 8, 0, 9, 0, "IMAGE"]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
}

with open(r"C:\Users\rohit\.gemini\antigravity-ide\brain\75ca5046-c050-4870-bd18-6c550995f008\Perfect_Pooja_Card_Flux.json", "w") as f:
    json.dump(workflow, f, indent=2)
