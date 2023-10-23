def detect_csharp_framework(file_content):
    if "<TargetFramework>netcoreapp" in file_content or "<TargetFramework>netstandard" in file_content:
        return ".NET Core"
    return ".NET Framework"
