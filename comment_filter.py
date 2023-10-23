import re

# Khả năng mở rộng cho filter_comments: Thay vì dựa vào số lượng ký tự bình luận để xác định cách lọc, hãy cố gắng thiết kế một cơ chế linh hoạt hơn. Ví dụ: bạn có thể định nghĩa cấu trúc dữ liệu cho từng loại bình luận (single-line, block start, block end) và xử lý dựa trên đó.


def filter_comments(lines, language, language_comments):
    comment_data = language_comments.get(language, {"single": [], "block": []})
    single_comments = comment_data["single"]
    block_comments = comment_data["block"]

    filtered_lines = []
    in_block_comment = False
    end_block_comment = None if not block_comments else block_comments[1]

    for line in lines:
        if not in_block_comment:
            if any(line.strip().startswith(sym) for sym in single_comments):
                continue
            if block_comments and block_comments[0] in line:
                in_block_comment = True
                line = re.sub(re.escape(block_comments[0]) + '.*$', '', line)
        if end_block_comment and end_block_comment in line:
            in_block_comment = False
            line = re.sub('^.*?' + re.escape(end_block_comment), '', line)
        if not in_block_comment and line.strip() != "":
            filtered_lines.append(line)

    return filtered_lines
