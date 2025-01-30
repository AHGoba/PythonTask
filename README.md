# Namaa Backend Challenge - Python Code Execution Server  
**Author**: {AhmedGoba}  
**Email**: {Ahmedhamdygoba@gmail.com}  

---

## 📋 **Implemented Levels**  
- ✅ **Level 1**: Basic Code Execution  
- ✅ **Level 2**: Resource Limits (Time/Memory)  
- ✅ **Level 3**: Persistent Interpreter Sessions  

---

## 🛠️ **Prerequisites**  
- Python 3.8+  
- `pip` (Python package manager)  

---

## 🚀 **Setup Instructions**  

### **Linux/MacOS**  
```bash
# Clone the repository (if applicable)
git clone {your_repository_url}
cd namaa-backend-solution

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py

### **Windows**
# Clone the repository (if applicable)
git clone {your_repository_url}
cd namaa-backend-solution

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py


🌐 API Endpoint
POST /execute
Request Body:
{
  "id": "string (optional)",  // Session ID (for Level 3)
  "code": "string"            // Python code to execute
}

Response:
{
  "id": "string",    // Session ID (for Level 3)
  "stdout": "string",
  "stderr": "string",
  "error": "string"
}

🧪 Testing Examples
Level 1-2 (Basic Execution + Limits)
curl -X POST http://localhost:5000/execute \
-H "Content-Type: application/json" \
-d '{"code": "print(\"Hello World!\")"}'
{"stdout": "Hello World!\n"}


