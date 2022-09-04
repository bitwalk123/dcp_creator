def is_num(s: str):
    """
    Reference
    https://note.nkmk.me/python-str-num-determine/

    :return: bool
    """
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True
