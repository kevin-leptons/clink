def build_template(text, values):
    r = text
    for k, v in values.items():
        r = r.replace(k, v)
    return r
