import os

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