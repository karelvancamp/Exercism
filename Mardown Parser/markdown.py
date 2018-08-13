import re

def mark_group(str_, mark):
    return f'<{mark}>{str_}</{mark}>'

def attribute(str_, pattern, mark):
    c = re.sub(pattern, mark_group(r'\2', mark), str_)
    return c

def italic(line):
    return attribute(line, '(_)(.*?)(_)', 'em')

def strong(line):
    return attribute(line, '(__)(.*?)(__)', 'strong')

def headers_or_paragraph(line):
    c = re.findall('^(#+) (.*)',line)
    if c:
        n = str(len(c[0][0]))
        return mark_group(c[0][1], f'h{n}')
    return mark_group(line, 'p')

def unordered_list(list_line):
    c = ''.join([mark_group(x, 'li') for x in list_line])
    return mark_group(c, 'ul')

def find_list(lines):
    c = []
    for x in lines:    
        if x[:2] == '* ':
            c.append(x[2:])
        elif c:
            yield c
            yield x
            c = []
        else:
            yield x
    if c:
        yield c
        
def parse_markdown(markdown):
    lines = [x for x in find_list(markdown.split('\n'))]
    outx = []
    for line in lines:
        if isinstance(line,list):
            line = unordered_list(line)
        else:
            line = headers_or_paragraph(line)
        outx.append( italic( strong(line)))
            
    return ''.join(outx)