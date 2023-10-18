import math

def display_chart_terminal(data, n):
    # Ký tự đặc biệt để vẽ chart
    full_block = "▓"
    empty_block = "░"
    
    # Lấy n ngôn ngữ và tính tổng phần trăm 
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    top_percentages = sum(item[1] for item in sorted_data)
    
    # Tính phần trăm còn lại với mục "Other"
    other_percentage = 100.0 - top_percentages
    if other_percentage > 0:
        sorted_data.append(('Other', other_percentage))
    
    # Biểu diễn chart dựa trên ký tự
    chart = ""
    total_blocks = 20  # Số ký tự dùng biểu diễn 100%
    
    for language, percentage in sorted_data:
        num_blocks = int((percentage / 100) * total_blocks)
        chart += full_block * num_blocks
        chart += empty_block * (total_blocks - num_blocks)
        chart += f" {language} ({percentage:.2f}%)"
        chart += "\n"
    
    print(chart)


if __name__ == "__main__":
    directory_path = "C:\\Users\\tinho\\OneDrive\\Desktop\\python-backend-template-master\\python-backend-template-master"
    lang_percentages = analyze_directory(directory_path)
    
    n = 3
    display_chart_terminal(lang_percentages, n)
