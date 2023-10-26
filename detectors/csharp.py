def detect_csharp_framework(file_content):
    if "<TargetFramework>netcoreapp" in file_content:
        return ".NET Core"
    elif "<TargetFramework>netstandard" in file_content:
        return ".NET Standard"
    elif "<TargetFramework>net" in file_content:
        return ".NET 5/6/7"
    return "Unknown"
