from flask import Flask, request, jsonify
import subprocess


# --name-- refer to the project name
# and according to the flask that can help me doing an web app
app = Flask(__name__)

#when i want to make a route I must put an (@) before the app then put the route then the method
@app.route('/execute', methods=['POST'])
#when reach the url run the function below
def execute_code():
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "Invalid request. Code is required."}), 400

    try:
        # ننفذ الكود باستخدام subprocess
        result = subprocess.run(
            ['python', '-c', code],  # ننفذ الكود باستخدام Python
            capture_output=True,      # نمسك الإخراج والأخطاء
            text=True                 # نحول الإخراج إلى نص
        )

        # نطبع الناتج علشان نتأكد من المشكلة
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)
        print("returncode:", result.returncode)

        # نرجع الناتج أو الخطأ
        if result.returncode == 0:  # لو الكود اتنفذ من غير أخطاء
            return jsonify({"stdout": result.stdout})
        else:  # لو كان فيه خطأ ساعتها بيطلع رقم غير الصفر
            return jsonify({"stderr": result.stderr}), 500
    except Exception as e:
        # نطبع الخطأ علشان نعرف إيه المشكلة
        print("Exception:", str(e))
        return jsonify({"stderr": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)