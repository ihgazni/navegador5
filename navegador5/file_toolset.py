from navegador5 import shell_cmd
import os


def write_to_file(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    fd.write(kwargs['content'])
    fd.close()
    
def read_file_content(**kwargs):
    fd = open(kwargs['fn'],kwargs['op'])
    rslt = fd.read()
    fd.close()
    return(rslt)


#mkdir
def mkdir(path,force=False):
    if(os.path.exists(path)):
        if(force):
            shell_cmd.pipe_shell_cmds({1:'rm -r '+path})
        else:
            pass
    else:
        os.makedirs(path)


