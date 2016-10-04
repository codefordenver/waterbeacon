def int_or_none(value):
    try:
        try:
            val = int(value)
        except ValueError:
            val = int(round(float(value))) # just in case we get a float
    except (ValueError, TypeError):
        val = None
    return val
