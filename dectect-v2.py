import os
import json
import fnmatch

def analyze_directory(directory):
    # Tỷ lệ phần trăm cho mỗi language
    lang_percentages = {}
    total_lines = 0

    # Dictionary "extension_to_language" để xác định language dựa trên phần mở rộng của file
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

    # Pattern cho comments dựa vào language
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

    # Duyệt qua mỗi file trong thư mục
    for root, dirs, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extension_to_language or file in extension_to_language:
                lang = extension_to_language.get(ext, extension_to_language.get(file))

                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    lines = filter_comments(lines, lang)
                    total_lines += len(lines)
                    lang_percentages[lang] = lang_percentages.get(lang, 0) + len(lines)

    # Chuyển số dòng code thành tỷ lệ phần trăm
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
    display_chart_terminal(lang_percentages, 3)
    
    print("\nDetected Frameworks:")
    for lang, framework in frameworks.items():
        print(f"{lang}: {framework}")

if __name__ == "__main__":
    directory_path = "C:\\Users\\tinho\\OneDrive\\Desktop\\newcore"
    frameworks_info = {
        "Python": {"requirements.txt": "Unknown Python Framework", "setup.py": "Unknown Python Framework"},
        "JavaScript": {"package.json": "Unknown JavaScript/TypeScript Framework"},
        "Java": {"pom.xml": "Maven", "build.gradle": "Gradle"},
        "PHP": {"composer.json": "Composer"},
        "C#": {}
        # Thêm các ngôn ngữ và file cấu hình tương ứng ở đây
    }
    
    lang_percentages = analyze_directory(directory_path)
    detected_frameworks = detect_framework(directory_path, frameworks_info)
    display_results(lang_percentages, detected_frameworks)
