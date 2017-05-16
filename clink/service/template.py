def build_tpl(file_path, values):
    f = open(file_path)
    data = f.read()
    f.close()

    for k, v in values.items():
        data = data.replace(k, v)

    return data
