import os
import fnmatch
import re
import collections

from detectors import detect_framework, detect_csharp_framework, detect_python_framework, detect_javascript_framework
from display import display_chart_terminal, display_results
from settings import load_comments_from_json, load_languages_from_json, load_config_from_json, load_settings_from_template
from language_classifier import classify_language


def analyze_directory(directory, extension_to_language, language_comments, ignore_files, ignore_dirs):
    lang_percentages = collections.defaultdict(int)
    total_lines = 0

    def filter_comments(lines, language):
        comment_symbols = language_comments.get(language, [])
        if not comment_symbols:
            return lines

        if len(comment_symbols) == 1:
            single_line_comment = re.compile(
                r'^\s*' + re.escape(comment_symbols[0]))
            return [line for line in lines if not single_line_comment.match(line)]

        elif len(comment_symbols) == 2:
            single_line_comment = re.compile(
                r'^\s*' + re.escape(comment_symbols[0]) + '|' + re.escape(comment_symbols[1]) + '\s*$')
            return [line for line in lines if not single_line_comment.match(line)]

        elif len(comment_symbols) == 3:
            start_block_comment = re.escape(comment_symbols[1])
            end_block_comment = re.escape(comment_symbols[2])
            single_line_comment = re.compile(
                r'^\s*' + re.escape(comment_symbols[0]) + '|' + end_block_comment + '\s*$')
            block_comment = re.compile(
                start_block_comment + '.*?' + end_block_comment, re.DOTALL)

            filtered_lines = []
            in_block_comment = False
            for line in lines:
                if not in_block_comment:
                    if single_line_comment.match(line):
                        continue
                    if start_block_comment in line:
                        in_block_comment = True
                        line = re.sub(start_block_comment + '.*$', '', line)
                if end_block_comment in line:
                    in_block_comment = False
                    line = re.sub('^.*?' + end_block_comment, '', line)
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
                            line_count = len(lines)
                            total_lines += line_count
                            lang_percentages[lang] += line_count

    scan_directory(directory)

    for lang in lang_percentages:
        lang_percentages[lang] = (lang_percentages[lang] / total_lines) * 100
    return dict(lang_percentages)


def analyze_projects(directory, frameworks_info, extension_to_language, language_comments, ignore_files, ignore_dirs, n, total_blocks):
    projects = [f.path for f in os.scandir(directory) if f.is_dir()]
    for project in projects:
        print(f"Analyzing project: {os.path.basename(project)}")
        lang_percentages = analyze_directory(
            project, extension_to_language, language_comments, ignore_files, ignore_dirs)
        detected_frameworks = detect_framework(project, frameworks_info)
        display_results(lang_percentages, detected_frameworks, n, total_blocks)
        print("\n" + "-"*50 + "\n")


def main():
    settings = load_settings_from_template()

    directory_path = settings["directory_path"]
    total_blocks = settings["total_blocks"]
    n = settings["n"]

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
                     language_comments, ignore_files, ignore_dirs, n, total_blocks)


if __name__ == "__main__":
    main()
