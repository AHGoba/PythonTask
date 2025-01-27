from flask import Flask, request, jsonify
import subprocess
import psutil

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "Invalid request. Code is required."}), 400

    try:
        # Time Limit: 2 seconds
        result = run_code_with_timeout(code, timeout=2)
        if result is None:
            return jsonify({"error": "execution timeout"}), 500

        # Memory Limit: 100 MB
        result = run_code_with_memory_limit(code, memory_limit=100)
        if result is None:
            return jsonify({"error": "memory limit exceeded"}), 500

        # نرجع الناتج أو الخطأ
        if result.returncode == 0:  # لو الكود اتنفذ من غير أخطاء
            return jsonify({"stdout": result.stdout})
        else:  # لو كان فيه خطأ
            return jsonify({"stderr": result.stderr}), 500
    except Exception as e:
        return jsonify({"stderr": str(e)}), 500

def run_code_with_timeout(code, timeout):
    try:
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        return None

def run_code_with_memory_limit(code, memory_limit):
    process = subprocess.Popen(
        ['python', '-c', code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    #لو العمليه حسب السعه اللى وخداها فى الميمورى اكترمن حد معين اققف لة تمام خلاص
    while process.poll() is None:
        memory_usage = psutil.Process(process.pid).memory_info().rss / (1024 * 1024)
        if memory_usage > memory_limit:
            process.terminate()
            return None

    stdout, stderr = process.communicate()
    return subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr)

if __name__ == '__main__':
    app.run(debug=True, port=5000)