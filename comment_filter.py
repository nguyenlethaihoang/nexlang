import re


def filter_comments(lines, language, language_comments):
    comment_symbols = language_comments.get(language, [])
    if not comment_symbols:
        return lines

    if len(comment_symbols) == 1:
        single_line_comment = re.compile(
            r'^\s*' + re.escape(comment_symbols[0]))
        return [line for line in lines if not single_line_comment.match(line)]

    elif len(comment_symbols) == 2:
        single_line_comment = re.compile(
            r'^\s*' + re.escape(comment_symbols[0]) + '|' + re.escape(comment_symbols[1]) + '\s*$')
        return [line for line in lines if not single_line_comment.match(line)]

    elif len(comment_symbols) == 3:
        start_block_comment = re.escape(comment_symbols[1])
        end_block_comment = re.escape(comment_symbols[2])
        single_line_comment = re.compile(
            r'^\s*' + re.escape(comment_symbols[0]) + '|' + end_block_comment + '\s*$')
        block_comment = re.compile(
            start_block_comment + '.*?' + end_block_comment, re.DOTALL)

        filtered_lines = []
        in_block_comment = False
        for line in lines:
            if not in_block_comment:
                if single_line_comment.match(line):
                    continue
                if start_block_comment in line:
                    in_block_comment = True
                    line = re.sub(start_block_comment + '.*$', '', line)
            if end_block_comment in line:
                in_block_comment = False
                line = re.sub('^.*?' + end_block_comment, '', line)
            if not in_block_comment:
                filtered_lines.append(line)

        return filtered_lines
