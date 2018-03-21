from navegador5 import shell_cmd
import os

import chardet

def convert_code(to_codec="UTF8",**kwargs):
    fd = open(kwargs['fn'],"rb+")
    rslt = fd.read()
    fd.close()
    from_codec = chardet.detect(rslt)['encoding']
    rslt = rslt.decode(from_codec).encode(to_codec)
    os.remove(kwargs['fn'])
    fd = open(kwargs['fn'],"wb+")
    fd.write(rslt)
    fd.close()


def write_to_file(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    fd.write(kwargs['content'])
    fd.close()
    
def read_file_content(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    rslt = fd.read()
    fd.close()
    return(rslt)

def prepend_to_file(prepend,**kwargs):
    prepend=bytes(prepend)
    fd = open(kwargs['fn'],"rb+")
    rslt = fd.read()
    fd.close()
    os.remove(kwargs['fn'])
    fd = open(kwargs['fn'],"wb+")
    fd.write(prepend+rslt)
    fd.close()


#mkdir
def mkdir(path,force=False):
    if(os.path.exists(path)):
        if(force):
            shell_cmd.pipe_shell_cmds({1:'rm -r '+path})
        else:
            pass
    else:
        os.makedirs(path)

#find all files recursively
def walkall_files(dirpath=os.getcwd()):
    fps = []
    for (root,subdirs,files) in os.walk(dirpath):
        for fn in files:
            path = os.path.join(root,fn)
            fps.append(path)
    return(fps)
