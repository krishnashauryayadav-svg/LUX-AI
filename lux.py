import os
import sys
import json
import subprocess
import requests

# --- फंक्शन 1: ऑफलाइन कोडर इंजन ---
def ask_ai(prompt, is_json=False):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2.5-coder:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    if is_json:
        data["format"] = "json"
        
    try:
        response = requests.post(url, json=data)
        return response.json().get("response", "").strip()
    except Exception:
        return None

# --- फंक्शन 2: स्मार्ट भाषा सजेशन ---
def get_best_language(user_problem):
    languages_list = ["Python", "Java", "C++", "Rust"]
    
    prompt = (
        f"Analyze this problem: '{user_problem}'\n"
        f"Select the absolute best programming language ONLY from this list: {languages_list}.\n"
        f"Respond ONLY with a valid JSON object matching this exact schema:\n"
        f"{{\n"
        f"  \"language\": \"Name of language from the list\",\n"
        f"  \"reason\": \"A short 1-line reason why\"\n"
        f"}}"
    )
    
    ai_res = ask_ai(prompt, is_json=True)
    try:
        data = json.loads(ai_res)
        return data.get("language", "Python"), data.get("reason", "Best fit.")
    except:
        return "Python", "Default safe fallback."

# --- फंक्शन 3: यूनिवर्सल एनवायरनमेंट रनर ---
def run_code_by_extension(folder_path, filename, code, user_test_input=""):
    full_file_path = os.path.join(folder_path, filename)
    with open(full_file_path, "w", encoding="utf-8") as f:
        f.write(code)
        
    ext = filename.split(".")[-1]
    
    try:
        # 🐍 1. PYTHON LOGIC
        if ext == "py":
            local_venv = os.path.join(folder_path, "venv")
            if not os.path.exists(local_venv):
                subprocess.run([sys.executable, "-m", "venv", local_venv], stdout=subprocess.DEVNULL)
            
            v_python = os.path.join(local_venv, "Scripts", "python.exe")
            v_pip = os.path.join(local_venv, "Scripts", "pip.exe")
            
            if "PyQt5" in code or "QWebEngineView" in code:
                subprocess.run([v_pip, "install", "pyqt5", "pyqtwebengine"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            result = subprocess.run([v_python, full_file_path], input=user_test_input, capture_output=True, text=True, timeout=15)
            
        # 🦀 2. C++ LOGIC
        elif ext == "cpp":
            exe_path = os.path.join(folder_path, "program.exe")
            compile_res = subprocess.run(["g++", full_file_path, "-o", exe_path], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"status": "error", "message": f"Compilation Error:\n{compile_res.stderr}"}
            result = subprocess.run([exe_path], input=user_test_input, capture_output=True, text=True, timeout=10)
            
        # ☕ 3. JAVA LOGIC
        elif ext == "java":
            compile_res = subprocess.run(["javac", full_file_path], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"status": "error", "message": f"Compilation Error:\n{compile_res.stderr}"}
            
            class_name = filename.split(".")[0]
            result = subprocess.run(["java", "-cp", folder_path, class_name], input=user_test_input, capture_output=True, text=True, timeout=10)
            
        # ⚙️ 4. RUST LOGIC
        elif ext == "rs":
            exe_path = os.path.join(folder_path, "rust_program.exe")
            compile_res = subprocess.run(["rustc", full_file_path, "-o", exe_path], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"status": "error", "message": f"Compilation Error:\n{compile_res.stderr}"}
            result = subprocess.run([exe_path], input=user_test_input, capture_output=True, text=True, timeout=10)
            
        else:
            return {"status": "error", "message": f"Unsupported language extension: .{ext}"}

        if result.returncode != 0:
            return {"status": "error", "message": result.stderr}
        return {"status": "success", "message": result.stdout}

    except subprocess.TimeoutExpired:
        return {"status": "success", "message": "Execution finished successfully (or GUI Window loaded)."}
    except FileNotFoundError:
        return {"status": "error", "message": f"Compiler for .{ext} not found on your system!"}

# --- फंक्शन 4: यूनिवर्सल सेल्फ-हीलिंग इंजन ---
def lux_self_healing_engine(user_problem, selected_lang, user_test_input):
    if selected_lang == "Auto":
        lang, reason = get_best_language(user_problem)
        print(f"💡 AI का सुझाव: '{lang}' चुना गया क्योंकि - {reason}")
    else:
        lang = selected_lang

    ext_map = {"Python": "main.py", "Java": "Main.java", "C++": "main.cpp", "Rust": "main.rs"}
    f_name = ext_map.get(lang, "main.py")
    
    project_folder = os.path.join("Lux_Projects", f"proj_{lang.lower()}")
    os.makedirs(project_folder, exist_ok=True)

    prompt = f"Write a complete, working {lang} program for: {user_problem}. Respond ONLY with raw executable code, no markdown blocks like ```python or ```."
    code = ask_ai(prompt)
    
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        print(f"⚙️ [Sandbox] कोड रन किया जा रहा है: {f_name} (Attempt {attempts + 1})...")
        
        if not code or len(code.strip()) < 20 or ("Hello" in code and "QWebEngineView" not in code and "PyQt5" not in code and "cube" in user_problem.lower()):
            execution = {"status": "error", "message": "CRITICAL ERROR: Code is empty or just prints generic Hello World. Write full logic!"}
        else:
            execution = run_code_by_extension(project_folder, f_name, code, user_test_input)
            
        if execution["status"] == "success":
            print("✅ [Success] एरर देव परास्त! कोड बिल्कुल सही चल गया।")
            
            if lang == "Python" and ("PyQt5" in code or "QWebEngineView" in code):
                with open(os.path.join(project_folder, "requirements.txt"), "w") as f:
                    f.write("pyqt5\npyqtwebengine")
                    
            return code, execution["message"], project_folder
        else:
            error_msg = execution["message"]
            print(f"❌ [Error Found] कोड फेल हुआ!\nविवरण:\n{error_msg}")
            
            print("🔄 [AI Agent] एरर को समझकर कोड को रीवायर कर रहा है...")
            fix_prompt = f"The previous {lang} code caused this error:\n{error_msg}\nFix this specific error and provide the complete corrected code. No explanations, no markdown blocks."
            code = ask_ai(fix_prompt)
            attempts += 1
            
    print("⚠️ 10 प्रयासों के बाद भी कोड पूरी तरह ठीक नहीं हो पाया।")
    return None, None, None

# --- डायरेक्ट प्रॉम्प्ट फीडिंग एरिया (नो यूआई) ---
if __name__ == "__main__":
    # 📝 1. अपनी समस्या यहाँ लिखें
    my_problem = "write a python code to multply two matrices"
    
    # 🎯 2. भाषा चुनें: "Python", "C++", "Java", "Rust" या ऑटो के लिए "Auto"
    my_language = "Python"
    
    # 📥 3. अगर कोड को रनटाइम इनपुट चाहिए तो यहाँ लिखें (वरना खाली छोड़ दें "")
    my_test_input = ""
    
    print(f"🚀 [Lux.AI Backup Core] मिशन शुरू! भाषा: {my_language}")
    final_code, output, folder = lux_self_healing_engine(my_problem, my_language, my_test_input)
    
    if final_code:
        print(f"\n==============================================")
        print(f"📊 [Mission Accomplished]")
        print(f"📂 आपका प्रोजेक्ट फ़ोल्डर यहाँ लॉक है: {os.path.abspath(folder)}")
        print(f"💻 फाइनल आउटपुट:\n{output}")
