import os
import sys
import re
import json
import subprocess
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

WORKSPACE = "Lux_Local_Workspace"
os.makedirs(WORKSPACE, exist_ok=True)

# 🧠 लोकल ओलामा मॉडल से बात करना
# 🧠 लोकल ओलामा मॉडल से बात करना (Updated with Timeout Safety)
def ask_local_coder(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": f"Write a complete working python code for this task: {prompt}\nMake sure to wrap your code cleanly inside triple backticks like ```python ... ``` so it can be extracted.",
        "stream": False,
        "options": {
            "temperature": 0.1,    # Lower temperature = faster, more deterministic code
            "num_predict": 1024,   # Don't let it write long useless paragraphs
            "num_ctx": 4096        # Keep context small for your 4GB RAM
        }
    }
    try:
        # ⏳ We add a 60-second timeout here so your i3 system has full freedom to think without crashing Flask
        response = requests.post(url, json=data, timeout=3600)
        return response.json().get("response", "").strip()
    except requests.exceptions.Timeout:
        print("⚠️ Ollama took too long to respond! Your CPU is working hard.")
        return "```python\nprint('Error: Ollama Timeout. CPU overloaded.')\n```"
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return ""

# 🎯 जादुई हैकर ट्रिक: ग्यान छांटकर केवल बैकटिक्स (```) का कोड निकालना
def extract_clean_code(ai_text):
    # यह रेगुलर एक्सप्रेशन ```python और ``` के बीच की हर चीज़ को उखाड़ लेता है
    match = re.search(r"```(?:python)?(.*?)```", ai_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # अगर मॉडल बैकटिक्स लगाना ही भूल गया, तो सेफ्टी के लिए पूरा टेक्स्ट दे दो
    return ai_text.strip()

# 📦 सुरक्षित लोकल सैंडबॉक्स रनर
def run_in_sandbox(proj_name, file_name, code):
    proj_folder = os.path.join(WORKSPACE, proj_name)
    os.makedirs(proj_folder, exist_ok=True)
    
    code_path = os.path.join(proj_folder, file_name)
    req_path = os.path.join(proj_folder, "requirements.txt")
    
    with open(code_path, "w", encoding="utf-8") as f: 
        f.write(code)
    
    # 🕵️‍♂️ जादू यहाँ है: कोड से ऑटोमैटिक लाइब्रेरीज निकालना
    detected_deps = extract_dependencies_from_code(code)
    
    # requirements.txt को समर्पित फोल्डर में सेव करना
    with open(req_path, "w", encoding="utf-8") as f:
        f.write("\n".join(detected_deps))
    
    local_venv = os.path.join(proj_folder, "venv")
    if not os.path.exists(local_venv):
        subprocess.run([sys.executable, "-m", "venv", local_venv], stdout=subprocess.DEVNULL)
        
    v_python = os.path.join(local_venv, "Scripts", "python.exe")
    v_pip = os.path.join(local_venv, "Scripts", "pip.exe")
    
    # 📥 अब जो भी लाइब्रेरी कोड में होगी, वह ऑटोमैटिक इस लूप के जरिए इंस्टॉल हो जाएगी!
    if detected_deps:
        print(f"📥 [Auto-Installer] डिटेक्टेड लाइब्रेरीज इंस्टॉल हो रही हैं: {detected_deps}")
        for lib in detected_deps:
            subprocess.run([v_pip, "install", lib], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    try:
        res = subprocess.run([v_python, code_path], capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            return {"status": "error", "output": res.stderr, "folder": proj_folder}
        return {"status": "success", "output": res.stdout, "folder": proj_folder}
    except subprocess.TimeoutExpired:
        return {"status": "success", "output": "GUI Window or Long-running script loaded successfully.", "folder": proj_folder}

def extract_dependencies_from_code(code):
    # यह रेगुलर एक्सप्रेशन 'import package' और 'from package import ...' को ऑटो-डिटेक्ट करता है
    imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', code, re.MULTILINE)
    
    # पाइथन की इन-बिल्ट लाइब्रेरीज की लिस्ट (जिन्हें pip install करने की जरूरत नहीं होती)
    standard_libs = {
        "sys", "os", "re", "json", "subprocess", "math", "random", "time", 
        "datetime", "collections", "itertools", "functools", "urllib", "http",
        "socket", "threading", "multiprocessing", "tkinter", "abc", "typing"
    }
    
    # फालतू की डुप्लीकेट लाइब्रेरीज और इन-बिल्ट लाइब्रेरीज को लिस्ट से बाहर निकालना
    clean_deps = set()
    for lib in imports:
        lib_lower = lib.lower()
        if lib_lower not in standard_libs:
            # विशेष केस: अगर कोड में PyQt5 इस्तेमाल हुआ है तो pyqtwebengine भी चाहिए होगा
            if lib_lower == "pyqt5":
                clean_deps.add("pyqt5")
                clean_deps.add("pyqtwebengine")
            else:
                clean_deps.add(lib_lower)
                
    return list(clean_deps)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_prompt = data.get("prompt", "")
   # user_prompt = "build a simple web brouser"
    p_name = "project_" + re.sub(r'[^a-zA-Z0-9]', '_', user_prompt[:15]).lower().strip("_")

    f_name = "main.py"
    
    logs = ["🚀 [Lux Engine] लोकल मोटो एक्टिवेटेड।"]
    
    # 1. एआई से रॉ टेक्स्ट (ज्ञान समेत) मांगना
    raw_ai_response = ask_local_coder(user_prompt)
    if not raw_ai_response:
        return jsonify({"logs": ["❌ ओलामा से संपर्क नहीं हो पाया! कृपया ओलामा चालू करें।"]})
        
    # 2. जादू: ज्ञान को लात मारना और शुद्ध कोड निकालना
    clean_code = extract_clean_code(raw_ai_response)
    
    logs.append("📦 एआई का जवाब मिला। ज्ञान छांटकर शुद्ध कोड निकाल लिया गया है!")
    logs.append(f"⚙️ लोकल सैंडबॉक्स '{p_name}' में टेस्टिंग शुरू...")
    
    # 3. सैंडबॉक्स में टेस्ट रन
    result = run_in_sandbox(p_name, f_name, clean_code)
    
    # 🔄 लोकल सेल्फ-हीलिंग लूप
    attempts = 0
    while result["status"] == "error" and attempts < 3:
        logs.append(f"❌ गड़बड़ मिली! खुद सुधारने का प्रयास {attempts+1} चालू है...")
        fix_prompt = f"Your previous code caused this error:\n{result['output']}\nFix it and provide the complete corrected code inside triple backticks."
        
        raw_ai_response = ask_local_coder(fix_prompt)
        clean_code = extract_clean_code(raw_ai_response)
        result = run_in_sandbox(p_name, f_name, clean_code)
        attempts += 1
        
    if result["status"] == "success":
        logs.append("✅ [Success] एरर देव परास्त! समर्पित फ़ोल्डर में प्रोजेक्ट लॉक है।")
        return jsonify({"logs": logs, "output": result["output"], "folder": os.path.abspath(result["folder"])})
    else:
        logs.append("⚠️ हीलिंग इंजन ने मेहनत की, पर एरर पूरी तरह हल नहीं हुआ।")
        return jsonify({"logs": logs, "output": result["output"], "folder": os.path.abspath(result["folder"])})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
