from flask import Flask, request, jsonify
from llama_cpp import Llama  # Make sure this is imported at the top

app = Flask(__name__)

# Load the LLaMA model
llm = Llama(
    model_path = "/home/fifefola/ai-tutor-models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")
    if not prompt:
        return jsonify({"response": "No message provided"}), 400

    response = llm(
        prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1
    )
    return jsonify({"response": response["choices"][0]["text"]})
if __name__ == "__main__":
    print("✅ Flask app is starting...")
    app.run(debug=True)
