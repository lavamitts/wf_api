import os


def get_sql(folder, filename):
    filename = "{filename}.sql".format(
        filename=filename
    )
    contents = get_file(folder, filename)
    contents = contents.replace("\n", " ")
    contents = contents.replace("% s", "%s")
    return contents


def get_csv(folder, filename):
    filename = "{filename}.csv".format(
        filename=filename
    )
    contents = get_file(folder, filename)
    return contents


def get_file(folder, filename):
    filename = os.path.join(folder, filename)
    f = open(filename, "r")
    contents = f.read()
    f.close
    return contents


def to_bool(s):
    if s is None:
        return False
    else:
        if isinstance(s, str):
            s = s.lower().strip()
            if s in ("true", "1", "-1", "y", "yes"):
                return True
            else:
                return False
        elif isinstance(s, int):
            if s == 0:
                return False
            else:
                return True
