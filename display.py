def display_chart_terminal(data, n, total_blocks):
    full_block = "▓"
    empty_block = "░"

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    top_percentages = sum(item[1] for item in sorted_data)

    other_percentage = 100.0 - top_percentages
    if other_percentage > 0:
        sorted_data.append(('Other', other_percentage))

    chart = ""

    for language, percentage in sorted_data:
        num_blocks = int((percentage / 100) * total_blocks)
        chart += full_block * num_blocks
        chart += empty_block * (total_blocks - num_blocks)
        chart += f" {language} ({percentage:.2f}%)"
        chart += "\n"

    print(chart)


def display_results(lang_percentages, frameworks, n, total_blocks):
    print("Language Statistics:")
    display_chart_terminal(lang_percentages, n, total_blocks)

    print("\nDetected Frameworks:")
    for lang, framework in frameworks.items():
        print(f"{lang}: {framework}")
