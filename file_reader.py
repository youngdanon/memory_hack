def txt_read(link):
    file = open(link, 'r')
    result_str = ""
    for line in file:
        result_str += line
    return result_str
