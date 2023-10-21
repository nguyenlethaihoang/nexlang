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
            if len(comment_symbols) == 1:
                if line.strip().startswith(comment_symbols[0]):
                    continue

            elif len(comment_symbols) == 2:
                if line.strip().startswith(comment_symbols[0]):
                    continue
                if comment_symbols[1] in line:
                    continue

            elif len(comment_symbols) == 3:
                if line.strip().startswith(comment_symbols[0]):
                    continue

                if line.strip().startswith(comment_symbols[1]):
                    in_block_comment = True
                    continue

                if comment_symbols[2] in line:
                    in_block_comment = False
                    continue

            if not in_block_comment:
                filtered_lines.append(line)

        return filtered_lines

    # Duyệt qua mỗi file trong thư mục
    for root, dirs, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extension_to_language:
                lang = extension_to_language[ext]

                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    lines = filter_comments(lines, lang)
                    total_lines += len(lines)
                    lang_percentages[lang] = lang_percentages.get(lang, 0) + len(lines)

    # Chuyển số dòng code thành tỷ lệ phần trăm
    for lang, count in lang_percentages.items():
        lang_percentages[lang] = (count / total_lines) * 100

    return lang_percentages

def display_chart_terminal(data, n):
    # Ký tự đặc biệt để vẽ chart - có thể thay đổi ký tự khác
    full_block = "▓"
    empty_block = "░"

    # Lấy n language và tính tổng phần trăm
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    top_percentages = sum(item[1] for item in sorted_data)

    # Tính phần trăm còn lại với mục "Other"
    other_percentage = 100.0 - top_percentages
    if other_percentage > 0:
        sorted_data.append(('Other', other_percentage))

    # Biểu diễn chart dựa trên ký tự
    chart = ""
    total_blocks = 20  # Số ký tự dùng biểu diễn 100%

    for language, percentage in sorted_data:
        num_blocks = int((percentage / 100) * total_blocks)
        chart += full_block * num_blocks
        chart += empty_block * (total_blocks - num_blocks)
        chart += f" {language} ({percentage:.2f}%)"
        chart += "\n"

    print(chart)


if __name__ == "__main__":
    directory_path = "C:\\Users\\tinho\\OneDrive\\Desktop\\006-CoreVPS-main"
    lang_percentages = analyze_directory(directory_path)
    n = 3
    display_chart_terminal(lang_percentages, n)
 