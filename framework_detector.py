import os
import fnmatch
import json

def detect_framework(directory, frameworks_info):
    detected_frameworks = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            content = read_file_content(file_path)
            for lang, config_files in frameworks_info.items():
                if lang == "C#":
                    if fnmatch.fnmatch(file, "*.csproj") or fnmatch.fnmatch(file, "*.sln"):
                        detected_frameworks[lang] = detect_csharp_framework(file_path, content)
                        break
                elif file in config_files:
                    if lang == "Python":
                        detected_frameworks[lang] = detect_python_framework(content)
                    elif lang == "JavaScript":
                        detected_frameworks[lang] = detect_javascript_framework(file_path, content)
                    else:
                        detected_frameworks[lang] = config_files[file]
                    break
    return detected_frameworks

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def detect_python_framework(content):
    if "flask" in content.lower():
        return "Flask"
    if "django" in content.lower():
        return "Django"
    # Thêm các kiểm tra cho các framework Python khác ở đây nếu cần
    return "Unknown Python Framework"

def detect_javascript_framework(file_path, content):
    try:
        package_json = json.loads(content)
        dependencies = package_json.get("dependencies", {})
        devDependencies = package_json.get("devDependencies", {})
        
        if "react" in dependencies or "react" in devDependencies:
            return "ReactJS"
        if "vue" in dependencies or "vue" in devDependencies:
            return "VueJS"
        if "angular" in dependencies or "angular" in devDependencies:
            return "Angular"
        if "express" in dependencies or "express" in devDependencies:
            return "Express (NodeJS)"
        if "koa" in dependencies or "koa" in devDependencies:
            return "Koa (NodeJS)"
        # Thêm các kiểm tra cho các framework JS/TS khác ở đây nếu cần
    except json.JSONDecodeError as e:
        print(f"Could not parse {file_path}: {e}")
    return "Unknown JavaScript/TypeScript Framework"

def detect_csharp_framework(file_path, content):
    lower_content = content.lower()
    
    if "<project sdk=\"microsoft.net.sdk\">" in lower_content:
        return ".NET Core"
    if "<project sdk=\"microsoft.net.sdk.web\">" in lower_content:
        return "ASP.NET Core"
    if "<project sdk=\"microsoft.net.sdk.worker\">" in lower_content:
        return ".NET Core Worker"
    # Thêm các kiểm tra cho các framework và version khác ở đây nếu cần