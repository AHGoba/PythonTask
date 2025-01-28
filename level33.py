from flask import Flask, request, jsonify
import uuid
import multiprocessing
import io
import sys

class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.input_queue = multiprocessing.Queue()
        self.output_queue = multiprocessing.Queue()
        self.globals = {}
        self.process = multiprocessing.Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            code = self.input_queue.get()
            if code == "exit":
                break
            try:
                # إنشاء buffer لالتقاط الإخراج
                output_buffer = io.StringIO()
                sys.stdout = output_buffer  # تحويل stdout إلى buffer

                # تنفيذ الكود
                exec(code, self.globals)

                # استعادة stdout الأصلي
                sys.stdout = sys.__stdout__

                # الحصول على الإخراج من buffer
                output = output_buffer.getvalue().strip()

                # إرسال الإخراج في الرد
                if output:
                    self.output_queue.put({"stdout": output})
                else:
                    self.output_queue.put({"stdout": "Code executed successfully."})
            except Exception as e:
                self.output_queue.put({"stderr": str(e)})

    def execute(self, code):
        self.input_queue.put(code)
        return self.output_queue.get()

    def get_variable(self, var_name):
        return self.globals.get(var_name, "Variable not found.")

    def close(self):
        self.input_queue.put("exit")
        self.process.join()

app = Flask(__name__)
sessions = {}

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    session_id = data.get('id')

    if not code:
        return jsonify({"error": "Invalid request. Code is required."}), 400

    if session_id:
        if session_id not in sessions:
            return jsonify({"error": "Session not found."}), 404
        session = sessions[session_id]
    else:
        session = Session()
        sessions[session.id] = session

    try:
        result = session.execute(code)
        result["id"] = session.id
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_variable', methods=['POST'])
def get_variable():
    data = request.json
    session_id = data.get('id')
    var_name = data.get('var_name')

    if not session_id or not var_name:
        return jsonify({"error": "Session ID and variable name are required."}), 400

    if session_id not in sessions:
        return jsonify({"error": "Session not found."}), 404

    session = sessions[session_id]
    value = session.get_variable(var_name)

    return jsonify({"id": session_id, "variable": var_name, "value": value})

if __name__ == '__main__':
    app.run(debug=True, port=5000)