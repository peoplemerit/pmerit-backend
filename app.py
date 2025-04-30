from flask import Flask, request, jsonify
from flask_cors import CORS
from lavis.models import load_model_and_preprocess
from PIL import Image
import torch
import io

app = Flask(__name__)
CORS(app)

# Load BLIP-2 model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
model, vis_processors, txt_processors = load_model_and_preprocess(
    name="blip2_opt",
    model_type="pretrain_opt2.7b",
    is_eval=True,
    device=device
)

@app.route("/api/image", methods=["POST"])
def analyze_image():
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["file"]
    raw_image = Image.open(io.BytesIO(image_file.read())).convert("RGB")
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

    # Default or optional question
    question = request.form.get("question", "What is happening in this image?")
    output = model.generate({"image": image, "text_input": question})

    return jsonify({"question": question, "response": output[0]})
