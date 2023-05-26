def parse_json(item):
    if item == "[]":
        return {}
    elif item[0] == "{" or item[0] == "[":
        is_list = item[0] == "["
        item = item[1:-1]
        result = {}
        result_list = []
        depth = 0
        in_quotes = False
        temp_str = ""
        key = ""
        value = ""

        for char in item:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            elif char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
            elif char == "\"":
                in_quotes = not in_quotes
            elif char == ":" and not in_quotes and depth == 0:
                key += temp_str[1:-1]
                temp_str = ""
                continue
            elif char == "," and not in_quotes and depth == 0 and not is_list:
                value += temp_str[1:-1]
                result[key] = value
                value = ""
                key = ""
                temp_str = ""
                continue
            elif char == "," and is_list and depth == 0:
                result_list.append(parse_json(temp_str))
                temp_str = ""
                continue
            elif char == ' ' and not in_quotes:
                continue

            temp_str += char

        if temp_str[0] == "'" or temp_str[0] == '"':
            result[key] = temp_str[1:-1]
        elif is_list:
            result_list.append(parse_json(temp_str))
        else:
            result[key] = parse_json(temp_str)
    else:
        return item

    if is_list:
        return result_list
    else:
        return result
