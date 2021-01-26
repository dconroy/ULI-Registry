

def format_uli(licensee):
    item = {}
    item = {
        "uli": str(licensee["_id"]),
        "email": hide_email(licensee["email"]),
        "firstname": licensee["firstname"],
        "lastname": licensee["lastname"],
        "license_data": licensee["license_data"],
        "nrds": licensee["nrds"]
    }
    return item

def hide_email(email):
    m = email.split('@')
    return f'{m[0][0]}{"*"*(len(m[0])-2)}{m[0][-1] if len(m[0]) > 1 else ""}@{m[1]}'


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

