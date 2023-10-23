def detect_python_framework(file_content):
    if "flask" in file_content:
        return "Flask"
    elif "django" in file_content:
        return "Django"
    return "Unknown Python Framework"
