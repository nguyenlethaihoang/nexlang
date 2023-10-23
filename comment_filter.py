import re
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
# Khả năng mở rộng cho filter_comments: Thay vì dựa vào số lượng ký tự bình luận để xác định cách lọc, hãy cố gắng thiết kế một cơ chế linh hoạt hơn. Ví dụ: bạn có thể định nghĩa cấu trúc dữ liệu cho từng loại bình luận (single-line, block start, block end) và xử lý dựa trên đó.


def map_language_to_pygments_alias(language_name):
    mapping = {
        "Microsoft Visual Studio Solution": None,  # Pygments does not support this
        # Add more mappings if needed
    }
    return mapping.get(language_name, language_name)


def filter_comments_with_pygments(lines, language):
    language_alias = map_language_to_pygments_alias(language)
    if not language_alias:
        return lines
    lexer = get_lexer_by_name(language.lower(), stripall=True)
    tokens = lexer.get_tokens('\n'.join(lines))

    filtered_code = []

    for token_type, content in tokens:
        if token_type not in (Token.Comment, Token.Comment.Multiline, Token.Comment.Preproc, Token.Comment.Single):
            filtered_code.extend(content.split('\n'))

    return [line for line in filtered_code if line.strip() != ""]


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
