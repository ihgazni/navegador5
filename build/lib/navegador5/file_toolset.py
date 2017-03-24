


def write_to_file(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    fd.write(kwargs['content'])
    fd.close()
    
def read_file_content(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    rslt = fd.read()
    fd.close()
    return(rslt)