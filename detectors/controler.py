import os


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
