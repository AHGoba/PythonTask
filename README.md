

---

```md
# Namaa Backend Challenge - Python Code Execution Server  

**Author**: Ahmed Goba  
**Email**: ahmedhamdygoba@gmail.com  

---

## 📋 Implemented Levels  
- ✅ **Level 1**: Basic Code Execution  
- ✅ **Level 2**: Resource Limits (Time/Memory)  
- ✅ **Level 3**: Persistent Interpreter Sessions  

---

## 🛠️ Prerequisites  
- Python 3.8+  
- `pip` (Python package manager)  

---

## 🚀 Setup Instructions  

### 🔹 **Linux/MacOS**  
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
```

### 🔹 **Windows**  
```powershell
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
```

---

## 🌐 API Endpoint  

### **POST /execute**  
#### **Request Body**  
```json
{
  "id": "string (optional)",  // Session ID (for Level 3)
  "code": "string"            // Python code to execute
}
```

#### **Response**  
```json
{
  "id": "string",    // Session ID (for Level 3)
  "stdout": "string",
  "stderr": "string",
  "error": "string"
}
```

---

## 🧪 Testing Examples  

### **Level 1-2 (Basic Execution + Limits)**  
```bash
curl -X POST http://localhost:5000/execute \
-H "Content-Type: application/json" \
-d '{"code": "print(\"Hello World!\")"}'
```
#### **Expected Response:**  
```json
{
  "stdout": "Hello World!\n"
}
```

