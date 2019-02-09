
def parse_usual_snip(s):

    if '=' in s:
        name, text = s.split('=', maxsplit=1)
    else:
        name, text = s, s
    return {'kind': 'line', 'name': name, 'text': text}


def parse_synwrite_snip(lines):

    if not lines: return
    t = lines[0].split('=', maxsplit=1)
    if t[0]!='name': return
    name = t[1]
    while lines[0]!='text=':
        del lines[0]
    del lines[0]
    if not lines: return
    text = lines[0]
    return {'kind': 'sw', 'name': name, 'text': text}
