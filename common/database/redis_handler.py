

def KeyMaker(*args, **kwargs) -> str:
    key = [str(i) for i in list(args)]
    for k, d in kwargs.items():
        key += f'{str(d)}'    
    return ":".join(key)

