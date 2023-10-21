import os
from directory_analyzer import analyze_directory
from framework_detector import detect_framework
from display_results import display_results

frameworks_info = {
    "Python": {"requirements.txt": "Unknown Python Framework", "setup.py": "Unknown Python Framework"},
    "JavaScript": {"package.json": "Unknown JavaScript/TypeScript Framework"},
    "Java": {"pom.xml": "Maven", "build.gradle": "Gradle"},
    "PHP": {"composer.json": "Composer"},
    "C#": {}
    # Thêm các ngôn ngữ và file cấu hình tương ứng ở đây
}

def analyze_projects(directory):
    projects = [f.path for f in os.scandir(directory) if f.is_dir()]
    for project in projects:
        print(f"Analyzing project: {os.path.basename(project)}")
        lang_percentages = analyze_directory(project)
        detected_frameworks = detect_framework(project, frameworks_info)
        display_results(lang_percentages, detected_frameworks)
        print("\n" + "-"*50 + "\n")
