from flask import Flask, request, jsonify, Response, url_for
from models.openelm_connector import query_openelm
from models.azure_openai_connector import query_azure_openai
from utils.streaming import stream_response
import random
import socket

app = Flask(__name__)


def get_lan_ip():
    """获取本机局域网IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个外部IP（不需要真的连通）
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


LAN_IP = get_lan_ip()


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])  # 获取完整聊天记录
    user_question = data.get("question")
    model_choice = data.get("model")
    is_plot_request = "please draw a plot" in user_question.lower()

    # 这里你可以将history存储到数据库或文件，或者仅用于上下文
    # 这里只是简单存储到变量
    chat_history = history

    # 只把最新问题发给模型
    if model_choice == "openELM":
        answer = query_openelm(user_question)
    elif model_choice == "azure openai":
        answer = query_azure_openai(user_question)
    else:
        return jsonify({"error": "Invalid model choice"}), 400

    # 随机返回一张图片（你可以根据实际业务逻辑返回不同图片）
    image_list = ["plane.png"]
    image_file = random.choice(image_list)
    image_url = url_for("static", filename=f"images/{image_file}", _external=True)

    if is_plot_request:
        return jsonify({"image_url": image_url, "answer": answer})
    else:
        return answer


if __name__ == "__main__":
    from models.openelm_connector import initialize_openelm_model

    initialize_openelm_model()
    app.run(debug=True, host="0.0.0.0", port=1234)
