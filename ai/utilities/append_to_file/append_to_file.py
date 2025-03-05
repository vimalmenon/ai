def append_to_file(file: str, data: str):
    with open(file, "a") as f:
        f.write(data)
        f.write("\n")
