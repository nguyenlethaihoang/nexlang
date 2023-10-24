import os
import fnmatch
import collections

from detectors import detect_framework, detect_csharp_framework, detect_python_framework, detect_javascript_framework
from display import display_chart_terminal, display_results
from settings import load_comments_from_json, load_languages_from_json, load_config_from_json, load_settings_from_template
from language_classifier import classify_language
# Importing filter_comments function
from comment_filter import filter_comments, filter_comments_with_pygments


def analyze_directory(directory, extension_to_language, language_comments, ignore_files, ignore_dirs, detect_algorithm):
    lang_percentages = collections.defaultdict(int)
    total_lines = 0

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

                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = [
                                    line for line in f if line.strip() != ""]
                                if detect_algorithm == 1:
                                    lines = filter_comments(
                                        lines, lang, language_comments)
                                elif detect_algorithm == 2:
                                    lines = filter_comments_with_pygments(
                                        lines, lang)

                                line_count = len(lines)
                                total_lines += line_count
                                lang_percentages[lang] += line_count
                        except IOError as e:
                            print(f"Error reading file {file_path}: {e}")

    scan_directory(directory)

    for lang in lang_percentages:
        lang_percentages[lang] = (lang_percentages[lang] / total_lines) * 100
    return dict(lang_percentages)


def analyze_projects(directory, frameworks_info, extension_to_language, language_comments, ignore_files, ignore_dirs, n, total_blocks, detect_algorithm):
    projects = [f.path for f in os.scandir(directory) if f.is_dir()]
    for project in projects:
        print(f"Analyzing project: {os.path.basename(project)}")
        lang_percentages = analyze_directory(
            project, extension_to_language, language_comments, ignore_files, ignore_dirs, detect_algorithm)
        detected_frameworks = detect_framework(project, frameworks_info)
        display_results(lang_percentages, detected_frameworks, n, total_blocks)
        print("\n" + "-"*50 + "\n")


def main():
    settings = load_settings_from_template()
    directory_path = settings["directory_path"]
    total_blocks = settings["total_blocks"]
    n = settings["n"]
    detect_algorithm = settings["detect_algorithm"]

    frameworks_info = {
        "Python": {"app.py": detect_python_framework, "manage.py": lambda _: "Django"},
        "JavaScript": {"package.json": detect_javascript_framework},
        "Java": {"pom.xml": lambda _: "Maven", "build.gradle": lambda _: "Gradle"},
        "PHP": {"composer.json": lambda _: "Composer"},
        "C#": {"App.config": lambda _: ".NET Framework", "Web.config": lambda _: ".NET Framework", "*.csproj": detect_csharp_framework, "*.sln": detect_csharp_framework}
    }
    extension_to_language = load_languages_from_json()
    language_comments = load_comments_from_json()
    config = load_config_from_json()
    ignore_files = config["ignore_files"]
    ignore_dirs = config["ignore_dirs"]

    analyze_projects(directory_path, frameworks_info, extension_to_language,
                     language_comments, ignore_files, ignore_dirs, n, total_blocks, detect_algorithm)


if __name__ == "__main__":
    main()
