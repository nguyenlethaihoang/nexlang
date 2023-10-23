import fnmatch


def classify_language(file_path, language):
    if language == "JavaScript":
        if fnmatch.fnmatch(file_path, "*.ts"):
            return "TypeScript"
        if fnmatch.fnmatch(file_path, "*.jsx"):
            return "ReactJS"
    return language
