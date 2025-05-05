from lavis.models import load_model_and_preprocess
from PIL import Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load BLIP-2 model (OPT 2.7B version)
model, vis_processors, txt_processors = load_model_and_preprocess(
    name="blip2_opt",
    model_type="pretrain_opt2.7b",
    is_eval=True,
    device=device
)

# Load an image
raw_image = Image.open("your_test_image.jpg").convert("RGB")
image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

# Ask a question
question = "What is happening in this image?"

# Inference
output = model.generate({"image": image, "text_input": question})

print("\n--- AI Tutor's Answer ---\n")
print(output[0])
