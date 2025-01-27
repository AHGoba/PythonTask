from flask import Flask, request, jsonify
import uuid
import multiprocessing
import queue

# تعريف كلاس Session علشان ننشئ جلسات مترابطة
class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())  # ننشئ UUID فريد
        self.input_queue = multiprocessing.Queue()  # queue علشان نرسل الأكواد
        self.output_queue = multiprocessing.Queue()  # queue علشان نستقبل النتائج
        self.process = multiprocessing.Process(target=self.run)  # ننشئ عملية جديدة
        self.process.start()  # نبدأ العملية

    def run(self):
        # ننفذ الكود في العملية
        while True:
            code = self.input_queue.get()  # نستقبل الكود من الـ queue
            if code == "exit":  # لو الكود هو "exit"، نوقف العملية
                break
            try:
                exec(code)  # ننفذ الكود
                self.output_queue.put({"stdout": "Code executed successfully."})
            except Exception as e:
                self.output_queue.put({"stderr": str(e)})

    def execute(self, code):
        self.input_queue.put(code)  # نرسل الكود للعملية
        return self.output_queue.get()  # نستقبل الناتج

    def close(self):
        self.input_queue.put("exit")  # نرسل إشارة إيقاف للعملية
        self.process.join()  # ننتظر العملية علشان تخلص


# إنشاء التطبيق
app = Flask(__name__)
sessions = {}  # dictionary علشان نحتفظ بالجلسات


# تحديد المسار (/execute)
@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    session_id = data.get('id')

    if not code:
        return jsonify({"error": "Invalid request. Code is required."}), 400

    if session_id:  # لو فيه session_id، نستخدم الجلسة الموجودة
        if session_id not in sessions:
            return jsonify({"error": "Session not found."}), 404
        session = sessions[session_id]
    else:  # لو مفيش session_id، ننشئ جلسة جديدة
        session = Session()
        sessions[session.id] = session

    try:
        result = session.execute(code)  # ننفذ الكود في الجلسة
        result["id"] = session.id  # نضيف الـ session_id للرد
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True, port=5000)