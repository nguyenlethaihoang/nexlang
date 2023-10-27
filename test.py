import os
import subprocess

def is_git_repository(directory):
    # Kiểm tra xem có tồn tại thư mục .git trong thư mục được chỉ định hay không
    return os.path.isdir(os.path.join(directory, ".git"))
 
def init_temp_git_repo(directory):
    subprocess.run(["git", "init"], cwd=directory)
    subprocess.run(["git", "add", "."], cwd=directory)
    subprocess.run(["git", "commit", "-m", "temp commit"], cwd=directory)
    subprocess.run(["git", "config", "--global", "user.email", "you@example.com"], cwd=directory)
    subprocess.run(["git", "config", "--global", "user.name", "Your Name"], cwd=directory)
    

def detect_languages_with_linguist(directory):
    init_temp_git_repo(directory)
    # Chạy github-linguist và lấy output
    result = subprocess.run(["github-linguist", directory], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Error running linguist: " + result.stderr)
    
    return result.stdout


def analyze_projects_in_directory(root_directory):
    project_languages = {}

    # Duyệt qua tất cả các thư mục con trong root_directory
    for subdir in os.listdir(root_directory):
        full_path = os.path.join(root_directory, subdir)
        if os.path.isdir(full_path):
            languages = detect_languages_with_linguist(full_path)
            if languages:  # Chỉ thêm vào nếu không phải là None
                project_languages[subdir] = languages

    return project_languages

# Ví dụ sử dụng
root_directory = "/home/brandon/detectors/project"
projects = analyze_projects_in_directory(root_directory)
for project, languages in projects.items():
    print(f"Project: {project}")
    print(languages)
    print("--------")
