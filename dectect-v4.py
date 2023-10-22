import os
import json
import fnmatch


def classify_language(file_path, language):
    if language == "JavaScript":
        if fnmatch.fnmatch(file_path, "*.ts"):
            return "TypeScript"
        if fnmatch.fnmatch(file_path, "*.jsx"):
            return "ReactJS"
    return language


def analyze_directory(directory, extension_to_language, language_comments, ignore_files, ignore_dirs):
    lang_percentages = {}
    total_lines = 0

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

    def scan_directory(directory):
        nonlocal total_lines
        for entry in os.scandir(directory):
            if entry.is_dir():
                dir_name = entry.name
                if not dir_name.startswith('.') and not any(fnmatch.fnmatch(dir_name, pattern) for pattern in ignore_dirs):
                    scan_directory(entry.path)
            elif entry.is_file():
                file_name = entry.name
                if not file_name.startswith('.') and not any(fnmatch.fnmatch(file_name, pattern) for pattern in ignore_files):
                    file_path = entry.path
                    _, ext = os.path.splitext(file_name)
                    if ext in extension_to_language or file_name in extension_to_language:
                        lang = extension_to_language.get(
                            ext, extension_to_language.get(file_name))
                        lang = classify_language(file_path, lang)

                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            lines = [
                                line for line in lines if line.strip() != ""]
                            lines = filter_comments(lines, lang)
                            total_lines += len(lines)
                            lang_percentages[lang] = lang_percentages.get(
                                lang, 0) + len(lines)

    scan_directory(directory)

    for lang, count in lang_percentages.items():
        lang_percentages[lang] = (count / total_lines) * 100
    return lang_percentages


def detect_framework(directory, frameworks_info):
    detected_frameworks = {}
    for lang in frameworks_info.keys():
        detected_frameworks[lang] = "Unknown"

    def scan_directory(directory):
        for entry in os.scandir(directory):
            if entry.is_file():
                for lang, config_files in frameworks_info.items():
                    for config_file, framework_detector in config_files.items():
                        if entry.name == config_file:
                            with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            detected_frameworks[lang] = framework_detector(
                                content)
                            break
            elif entry.is_dir():
                scan_directory(entry.path)

    scan_directory(directory)
    return detected_frameworks


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


def analyze_projects(directory, frameworks_info, extension_to_language, language_comments, ignore_files, ignore_dirs):
    projects = [f.path for f in os.scandir(directory) if f.is_dir()]
    for project in projects:
        print(f"Analyzing project: {os.path.basename(project)}")
        lang_percentages = analyze_directory(
            project, extension_to_language, language_comments, ignore_files, ignore_dirs)
        detected_frameworks = detect_framework(project, frameworks_info)
        display_results(lang_percentages, detected_frameworks)
        print("\n" + "-"*50 + "\n")


def main():
    directory_path = "C:\\Users\\tinho\\OneDrive\\Desktop\\project"
    frameworks_info = {
        "Python": {"app.py": detect_python_framework, "manage.py": lambda _: "Django"},
        "JavaScript": {"package.json": detect_javascript_framework},
        "Java": {"pom.xml": lambda _: "Maven", "build.gradle": lambda _: "Gradle"},
        "PHP": {"composer.json": lambda _: "Composer"},
        "C#": {"App.config": lambda _: ".NET Framework", "Web.config": lambda _: ".NET Framework", "*.csproj": detect_csharp_framework, "*.sln": detect_csharp_framework}
    }
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
        "PHP": ['//', '/*', '*/'],
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
    ignore_files = ["package-lock.json", "yarn.lock", ".DS_Store"]
    ignore_dirs = ["node_modules", "__pycache__", ".git"]

    analyze_projects(directory_path, frameworks_info, extension_to_language,
                     language_comments, ignore_files, ignore_dirs)


def detect_python_framework(file_content):
    if "flask" in file_content:
        return "Flask"
    elif "django" in file_content:
        return "Django"
    return "Unknown Python Framework"


def detect_javascript_framework(file_content):
    try:
        package_json = json.loads(file_content)
        dependencies = package_json.get("dependencies", {})
        dev_dependencies = package_json.get("devDependencies", {})
        all_dependencies = {**dependencies, **dev_dependencies}

        if "react" in all_dependencies:
            return "React"
        elif "vue" in all_dependencies:
            return "Vue.js"
        elif "angular" in all_dependencies:
            return "Angular"
    except json.JSONDecodeError:
        print("Error: Could not parse package.json")
        return "Unknown"


def detect_csharp_framework(file_content):
    if "<TargetFramework>netcoreapp" in file_content or "<TargetFramework>netstandard" in file_content:
        return ".NET Core"
    return ".NET Framework"


if __name__ == "__main__":
    main()
