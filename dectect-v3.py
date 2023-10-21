import os
import json
import fnmatch
import re

def classify_language(file_path, language):
    if language == "JavaScript":
        if fnmatch.fnmatch(file_path, "*.ts"):
            return "TypeScript"
        if fnmatch.fnmatch(file_path, "*.jsx"):
            return "ReactJS"
    return language

def analyze_directory(directory):
    lang_percentages = {}
    total_lines = 0

    extension_to_language = {
        ".py": "Python",
        ".js": "JavaScript",
        ".html": "HTML",
        ".php": "PHP",
        ".java": "Java",
        ".css": "CSS",
        ".md": "Markdown",
        ".json": "JSON",
        ".cs": "C#",
        ".yml": "YAML",
        ".ps1": "Powershell",
        "Dockerfile": "Dockerfile",
        ".sln": "Microsoft Visual Studio Solution",
        ".xml": "XML",
        ".sh": "Shell"
    }

    language_comments = {
        "Python": ['#'],
        "JavaScript": ['//', '/*', '*/'],
        "HTML": ['<!--', '-->'],
        "PHP": ['//', '#', '/*', '*/'],
        "Java": ['//', '/*', '*/'],
        "CSS": ['/*', '*/'],
        "Markdown": [],
        "JSON": [],
        "C#": ['//', '/*', '*/'],
        "YAML": ['#'],
        "Powershell": ['#'],
        "Dockerfile": ['#'],
        "Microsoft Visual Studio Solution": [],
        "XML": ['<!--', '-->'],
        "Shell": ['#']
    }

    def filter_comments(lines, language):
        comment_symbols = language_comments.get(language, [])
        if not comment_symbols:
            return lines

        in_block_comment = False
        filtered_lines = []
        for line in lines:
            stripped_line = line.strip()
            if len(comment_symbols) == 1:
                if stripped_line.startswith(comment_symbols[0]):
                    continue

            elif len(comment_symbols) == 2:
                if stripped_line.startswith(comment_symbols[0]) or stripped_line.endswith(comment_symbols[1]):
                    continue

            elif len(comment_symbols) == 3:
                if stripped_line.startswith(comment_symbols[0]) or stripped_line.endswith(comment_symbols[2]):
                    continue

                if stripped_line.startswith(comment_symbols[1]):
                    in_block_comment = True
                    continue

                if stripped_line.endswith(comment_symbols[2]):
                    in_block_comment = False
                    continue

            if not in_block_comment:
                filtered_lines.append(line)

        return filtered_lines

    ignore_files = ["package-lock.json", "yarn.lock", "*.tmp", "*.log", "README.md", "package.json"]
    ignore_dirs = [".git", "node_modules", ".vscode", "__pycache__", "public"]

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_dirs)]
        files = [f for f in files if not f.startswith('.') and not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_files)]  
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            if ext in extension_to_language or file in extension_to_language:
                lang = extension_to_language.get(ext, extension_to_language.get(file))
                lang = classify_language(file_path, lang)

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    lines = [line for line in lines if line.strip() != ""]
                    lines = filter_comments(lines, lang)
                    total_lines += len(lines)
                    lang_percentages[lang] = lang_percentages.get(lang, 0) + len(lines)

    for lang, count in lang_percentages.items():
        lang_percentages[lang] = (count / total_lines) * 100

    return lang_percentages

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
    lower_content = content.lower()

    # Tìm kiếm các dấu hiệu đặc trưng của Flask
    if re.search(r"from flask", lower_content) or \
       re.search(r"flask\(", lower_content):
        return "Flask"

    # Tìm kiếm các dấu hiệu đặc trưng của Django
    if re.search(r"from django", lower_content) or \
       re.search(r"INSTALLED_APPS", lower_content):
        return "Django"

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
    
    print("Checking file:", file_path)
    print("Content:", lower_content)

    if "<project sdk=\"microsoft.net.sdk\">" in lower_content:
        return ".NET Core"
    if "<project sdk=\"microsoft.net.sdk.web\">" in lower_content:
        return "ASP.NET Core"
    if "<project sdk=\"microsoft.net.sdk.worker\">" in lower_content:
        return ".NET Core Worker"
    if re.search(r"<targetframeworkversion>v4\.5</targetframeworkversion>", lower_content):
        return ".NET Framework 4.5"
    # Thêm các kiểm tra cho các framework và version khác ở đây nếu cần
    
    return "Unknown C# Framework"


def display_chart_terminal(data, n):
    full_block = "▓"
    empty_block = "░"

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    top_percentages = sum(item[1] for item in sorted_data)

    other_percentage = 100.0 - top_percentages
    if other_percentage > 0:
        sorted_data.append(('Other', other_percentage))

    chart = ""
    total_blocks = 20

    for language, percentage in sorted_data:
        num_blocks = int((percentage / 100) * total_blocks)
        chart += full_block * num_blocks
        chart += empty_block * (total_blocks - num_blocks)
        chart += f" {language} ({percentage:.2f}%)"
        chart += "\n"

    print(chart)

def display_results(lang_percentages, frameworks):
    print("Language Statistics:")
    display_chart_terminal(lang_percentages, 5)
    
    print("\nDetected Frameworks:")
    for lang, framework in frameworks.items():
        print(f"{lang}: {framework}")

def analyze_projects(directory):
    projects = [f.path for f in os.scandir(directory) if f.is_dir()]
    for project in projects:
        print(f"Analyzing project: {os.path.basename(project)}")
        lang_percentages = analyze_directory(project)
        detected_frameworks = detect_framework(project, frameworks_info)
        display_results(lang_percentages, detected_frameworks)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    directory_path = "C:\\Users\\tinho\\OneDrive\\Desktop\\project"
    frameworks_info = {
        "Python": {"app.py": "Unknown Python Framework", "manage.py": "Django"},
        "JavaScript": {"package.json": "Unknown JavaScript/TypeScript Framework"},
        "Java": {"pom.xml": "Maven", "build.gradle": "Gradle"},
        "PHP": {"composer.json": "Composer"},
        "C#": {"App.config": ".NET Framework", "Web.config": ".NET Framework"}
        # Thêm các ngôn ngữ và file cấu hình tương ứng ở đây
    }
    
    analyze_projects(directory_path)
