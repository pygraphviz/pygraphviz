def stringify(agraph):
    result = agraph.string().split()
    if '""' in result:
        result.remove('""')

    some = " ".join(result)
    while " ]" in some:
        some = some.replace(" ]", "]")
    if "\\N" in some:
        num_nattrs = len(agraph.node_attr)
        if num_nattrs == 1:
            some = some.replace('node [label="\\N"];', "")
        else:
            if "[label" in some:
                some = some.replace('[label="\\N", ', "[")
            else:
                some = some.replace(', label="\\N"', "")
    result = some.split()
    return " ".join(result)
