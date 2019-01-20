example_dict = { 'key1' : 'value1',
                 'key2' : 'value2',
                 'key3' : { 'key3a': 'value3a' },
                 'key4' : { 'key4a': { 'key4aa': 'value4aa',
                                       'key4ab': 'value4ab',
                                       'key4ac': 'value4ac'},
                            'key4b': 'value4b'}
                }

def find_key(d, value):
    for k,v in d.items():
        if isinstance(v, dict):
            p = find_key(v, value)
            if p:
                return [k] + p
        elif v == value:
            return [k]

print(find_key(example_dict,'value4ac'))
