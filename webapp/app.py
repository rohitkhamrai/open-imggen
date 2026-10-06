from flask import Flask, request, jsonify, render_template, send_file
import urllib.request
import urllib.parse
import json
import random
import io

app = Flask(__name__)
SERVER_ADDRESS = "192.168.0.134:8188"

@app.route("/")
def index():
    return render_template("index.html", server_ip="192.168.0.134")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt_text = data.get("prompt", "Yajna card")
    client_id = data.get("client_id")
    
    with open("workflow_api.json", "r") as f:
        workflow = json.load(f)
        
    workflow["5"]["inputs"]["text"] = prompt_text + ", beautiful hindu pooja card, intricate details, 8k resolution, photorealistic"
    workflow["7"]["inputs"]["seed"] = random.randint(1, 999999999)
    
    p = {"prompt": workflow, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    req.add_header('Content-Type', 'application/json')
    try:
        res = urllib.request.urlopen(req)
        return jsonify(json.loads(res.read()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/history/<prompt_id>")
def history(prompt_id):
    try:
        req = urllib.request.Request(f"http://{SERVER_ADDRESS}/history/{prompt_id}")
        res = urllib.request.urlopen(req)
        return jsonify(json.loads(res.read()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/view/<filename>")
def view_image(filename):
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/view?filename={urllib.parse.quote(filename)}")
    try:
        res = urllib.request.urlopen(req)
        return send_file(io.BytesIO(res.read()), mimetype='image/png')
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
