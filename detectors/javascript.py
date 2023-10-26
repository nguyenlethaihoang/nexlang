import json


def detect_javascript_framework(file_content):
    try:
        package_json = json.loads(file_content)
        dependencies = package_json.get("dependencies", {})
        dev_dependencies = package_json.get("devDependencies", {})
        all_dependencies = {**dependencies, **dev_dependencies}

        if "react" in all_dependencies:
            return "React"
        elif "vue" in all_dependencies:
            return "Vue.js"
        elif "angular" in all_dependencies:
            return "Angular"
        elif "express" in all_dependencies:
            return "Node.js"
    except json.JSONDecodeError:
        print("Error: Could not parse package.json")
        return "Unknown"
