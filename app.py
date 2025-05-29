from flask import Flask, request, jsonify
import gpt4free
from gpt4free import Provider, ChatCompletion, ImageCompletion
import uuid

app = Flask(__name__)

# حافظه مکالمات به تفکیک کاربر
conversations = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    role = data.get('role', 'user')
    model = data.get('model', 'gpt-4')  # پیش‌فرض مدل

    if not user_id or not message:
        return jsonify({"error": "پارامترهای user_id و message اجباری هستند"}), 400

    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append({"role": role, "content": message})

    if role == 'user':
        try:
            response = ChatCompletion.create(
                provider=Provider.You,  # یا Provider.GPTChat if needed
                model=model,
                messages=conversations[user_id]
            )
            reply = str(response)
            conversations[user_id].append({"role": "assistant", "content": reply})
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": f"خطا در پاسخ مدل: {str(e)}"}), 500

    return jsonify({"status": "پیام با رول ذخیره شد، پاسخ تولید نشد."})


@app.route('/image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "پارامتر prompt اجباری است"}), 400

    try:
        image_url = ImageCompletion.create(
            provider=Provider.You,  # استفاده از you.com برای ساخت تصویر
            prompt=prompt
        )
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": f"خطا در ساخت تصویر: {str(e)}"}), 500

@app.route('/')
def home():
    return "✅ API چت‌بات فعال است."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
