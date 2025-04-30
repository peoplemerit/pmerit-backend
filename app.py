from llama_cpp import Llama  # Make sure this is at the top of your file

# Load the LLaMA model once (adjust path and context if needed)
llm = Llama(
    model_path="/home/pmerit4uwefunwa/ai-tutor-models/TinyLlama-1.1B-Chat-v1.0.gguf", 
    n_ctx=2048,
    n_threads=4
)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")
    if not prompt:
        return jsonify({"response": "No message provided"}), 400

    response = llm(prompt)
    return jsonify({"response": response["choices"][0]["text"]})
