import os
import fnmatch


def detect_framework(directory, frameworks_info):
    detected_frameworks = {}
    for lang in frameworks_info.keys():
        detected_frameworks[lang] = []

    def scan_directory(directory):
        for entry in os.scandir(directory):
            if entry.is_file():
                for lang, config_files in frameworks_info.items():
                    for config_pattern, framework_detector in config_files.items():
                        if fnmatch.fnmatch(entry.name, config_pattern):
                            with open(entry.path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            framework_detected = framework_detector(content)
                            if framework_detected not in detected_frameworks[lang] and framework_detected != "Unknown":
                                detected_frameworks[lang].append(
                                    framework_detected)
            elif entry.is_dir():
                scan_directory(entry.path)

    scan_directory(directory)
    return {k: ', '.join(v) if v else "Unknown" for k, v in detected_frameworks.items()}
