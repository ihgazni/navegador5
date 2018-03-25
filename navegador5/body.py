from navegador5 import head
from navegador5 import url_tool
import jsbeautifier
import urllib.parse
import gzip
import zlib
#zlib = deflate
import brotli
#brotli = br
import json
from lxml import etree
import lxml.html
import base64
import re
import os
#for show 
from xdict.cmdline import Hentry

##
## API NAME  IS    I-M-P-O-R-T-A-N-T !!! 
## refer to MDN API NAME
##          XPATH axis NAME
##          jQuery API NAME 
##people like instinctive , and then like their custom.          
##          people's instinctive meaning, the word meaning of word! dont do futher as possible as you can!
##

def text_cond(text,condmatch,*args):
    if(type(condmatch)==type("")):
        if(condmatch in text):
            return(True)
        else:
            return(False)
    elif(type(condmatch) == type(re.compile(""))):
        m = condmatch.search(text)
        if(m):
            return(true)
        else:
            return(False)
    else:
        return(condmatch(text,*args))

######

def get_html_text(info_container,**kwargs):
    '''
        要实现Content-Type的优先级
        header 中的
        body meta 中的
        
    '''
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type("")):
        html_text = info_container
    elif(type(info_container) == type(b'')):
        html_text = info_container.decode(coding)
    elif(type(info_container) == type(dict({}))):
        html_text = info_container['resp_body_bytes'].decode(coding)
    else:
        pass
    return(html_text)

def show_resp_body(ic,tag='html',**kwargs):
    html_text = get_html_text(ic,**kwargs)
    htry = Hentry(html_text=html_text)
    html_entry = htry.query(tag,**kwargs)
    if('only_print' in kwargs):
        only_print = kwargs['only_print']
    else:
        only_print = True
    if(only_print):
        return(None)
    else:
        return(html_entry)

def get_etree_root(info_container,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type("")):
        html_text = info_container
    elif(type(info_container) == type(b'')):
        html_text = info_container.decode(coding)
    elif(type(info_container) == type(dict({}))):
        html_text = info_container['resp_body_bytes'].decode(coding)
    else:
        pass
    root = etree.HTML(html_text)
    return(root)
###

def get_eles_via_xpath(info_container,xpath,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    return(eles)


def get_eles_via_xpath_textCond(info_container,xpath,*args,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('cond' in kwargs):
        cond = kwargs['cond']
    else:
        cond = ''
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    rslt = [] 
    eles = root.xpath(xpath)
    for i in range(0,eles.__len__()):
        if(text_cond(eles[i].text,cond,*args)):
            rslt.append(eles[i])
        else:
            pass
    return(rslt)

def get_eles_via_xpath_tailCond(info_container,xpath,*args,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('cond' in kwargs):
        cond = kwargs['cond']
    else:
        cond = ''
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    rslt = []
    eles = root.xpath(xpath)
    for i in range(0,eles.__len__()):
        if(text_cond(eles[i].tail,cond,*args)):
            rslt.append(eles[i])
        else:
            pass
    return(rslt)


def get_eles_via_xpath_iterTextCond(info_container,xpath,*args,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('cond' in kwargs):
        cond = kwargs['cond']
    else:
        cond = ''
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    rslt = []
    eles = root.xpath(xpath)
    for i in range(0,eles.__len__()):
        if(text_cond(etree_get_text(eles[i]),cond,*args)):
            rslt.append(eles[i])
        else:
            pass
    return(rslt)




def get_eles_via_xpath_attribValueCond(info_container,xpath,*args,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('cond' in kwargs):
        cond = kwargs['cond']
    else:
        cond = ''
    if('attri_bname' in kwargs):
        attribname = kwargs['attrib_name']
    else:
        attribname = ''
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    rslt = []
    eles = root.xpath(xpath)
    for i in range(0,eles.__len__()):
        if(text_cond(eles[i].get(attribname),cond,*args)):
            rslt.append(eles[i])
        else:
            pass
    return(rslt)


def get_eles_via_xpath_attribNameCond(info_container,xpath,*args,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('cond' in kwargs):
        cond = kwargs['cond']
    else:
        cond = ''
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    rslt = []
    eles = root.xpath(xpath)
    for i in range(0,eles.__len__()):
        keys = eles[i].attrib.keys()
        for attribname in keys:
            if(text_cond(eles[i].get(attribname),cond,*args)):
                rslt.append(eles[i])
                break
            else:
                pass
    return(rslt)





def get_preceding_siblings_via_xpath(info_container,xpath):
    '''return a  nested "array in array"'''
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = precedingSiblings(node)
        rslt.append(ele)
    return(rslt)


def get_preceding_siblings_via_xpath_flat(info_container,xpath,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    xpath = xpath.rstrip('/')+'/preceding-sibling::*'
    eles = root.xpath(xpath)
    return(eles)



def get_following_siblings_via_xpath(info_container,xpath):
    '''return a  nested "array in array"'''
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = followingSiblings(node)
        rslt.append(ele)
    return(rslt)



def get_following_siblings_via_xpath_flat(info_container,xpath,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    xpath = xpath.rstrip('/')+'/following-sibling::*'
    eles = root.xpath(xpath)
    return(eles)



#

def get_next_siblings_via_xpath(info_container,xpath,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = nextSibling(eles[i])
        rslt.append(ele) 
    return(rslt)

get_right_siblings_via_xpath = get_next_siblings_via_xpath
get_rsibs_via_xpath = get_next_siblings_via_xpath

def get_previous_siblings_via_xpath(info_container,xpath,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = previousSibling(eles[i])
        rslt.append(ele)    
    return(rslt)

get_left_siblings_via_xpath = get_previous_siblings_via_xpath
get_lsibs_via_xpath = get_previous_siblings_via_xpath


def get_which_sibling_via_xpath(info_container,xpath,which,**kwargs):
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('backwards' in kwargs):
        backwards = kwargs['backwards']
    else:
        backwards = 0
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = getSibling(node,which=which,backwards=backwards)
        rslt.append(ele)
    return(rslt)



def get_all_siblings_via_xpath(info_container,xpath,**kwargs):
    '''return a  nested "array in array"'''
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if('include_self' in kwargs):
        include_self = kwargs['include_self']
    else:
        include_self = 0
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = allSiblings(node,include_self=include_self)
        rslt.append(ele)
    return(rslt)



def get_some_siblings_via_xpath(info_container,xpath,seq_list,**kwargs):
    '''return a  nested "dict in array in array"'''
    if('coding' in kwargs):
        coding = kwargs['coding']
    else:
        coding = 'utf-8'
    if(type(info_container) == type(dict({}))):
        root = get_etree_root(info_container,coding=coding)
    else:
        root = info_container
    eles = root.xpath(xpath)
    rslt =[]
    for i in range(0,eles.__len__()):
        ele = someSiblings(node,seq_list)
        rslt.append(ele)
    return(rslt)


 





##

##
def etree_is_leaf_node(node):
    if(node.getchildren().__len__() == 0):
        return(True)
    else:
        return(False)


def etree_get_text(ele):
    '''     <Why need itertext? >  
        >>>html_text = '<html><body>TEXT<br/>TAIL</body></html>'
        >>>root = etree.HTML(html_text)
        >>>eles = root.xpath("//html/body")
        >>>eles[0].text
        'TEXT'
        >>>eles[0].tail == None
        True
        >>> nvbody.etree_get_text(eles[0])
        'TEXTTAIL'
        >>>
        >>>
        >>> eles = root.xpath("//html/body/br")
        >>> eles[0].text == None
        True
        >>> eles[0].tail
        'TAIL'
        >>> nvbody.etree_get_text(eles[0])
        ''
    >>>
    '''    
    it = ele.itertext()
    texts = list(it)
    text = ''
    for i in range(0,texts.__len__()):
        text = text + texts[i]
    return(text)

etree_itertext = etree_get_text


def etree_path_array(node,include_self=1):
    parr = [each.tag for each in node.iterancestors()]
    parr.reverse()
    if(include_self == 1):
        parr.append(node.tag)
    else:
        pass
    return(parr)


def etree_patharray_to_xpathstr(path_array):
    xpath_str = '/'
    for each in path_array:
        xpath_str = xpath_str + '/' + each
    return(xpath_str)



def etree_ancestor_depth(node,include_self=1):
    d = etree_path_array(node).__len__()
    if(include_self == 1):
        return(d)
    else:
        return(d-1)


def etree_descedants_depth(node,withpathinfo=0):
    depth = 0
    unhandled = [node]
    next_unhandled = []
    while(unhandled.__len__()>0):
        depth = depth + 1
        results = []
        for i in range(0,unhandled.__len__()):
            each_node = unhandled[i]
            children = each_node.getchildren()
            if(children.__len__() == 0):
                patharr = etree_path_array(each_node,include_self=1)
                results.append(patharr)
            else:
                next_unhandled = next_unhandled + children
        unhandled = next_unhandled
        next_unhandled = []
    if(withpathinfo):
        return({'depth':depth, 'paths':results})
    else:
        return(depth)


#####

def etree_siblings_info(node):
    parent = node.getparent()
    children = parent.getchildren()
    total = children.__len__()
    for i in range(0,total):
        if(node == children[i]):
            curr_seq = i
        else:
            pass
    return({'total':total,'seq':curr_seq,'parent':parent,'siblings':children})


def etree_get_sibling(node,which,backwards=1):
    parent = node.getparent()
    children = parent.getchildren()
    total = children.__len__()
    for i in range(0,total):
        if(node == children[i]):
            curr_seq = i
            break
        else:
            pass
    if(backwards):
        seq = curr_seq - which
    else:
        seq = curr_seq + which
    if((seq <0) | (seq > (total - 1))):
        return(None)
    else:
        return(children[seq])

getSibling = etree_get_sibling
sibling = etree_get_sibling

def nextSibling(node):
    return(etree_get_sibling(node,1,backwards=0))

rightSibling = nextSibling
rsib = nextSibling

def previousSibling(node):
    return(etree_get_sibling(node,1,backwards=1))

leftSibling = previousSibling
lsib = previousSibling

def followingSiblings(node):
    info = etree_siblings_info(node)
    seq = info['seq']
    children = info['siblings']
    return(children[(seq+1):])


def precedingSiblings(node):
    info = etree_siblings_info(node)
    seq = info['seq']
    children = info['siblings']
    return(children[0:seq])

def someSiblings(node,seq_list):
    rslt = []
    parent = node.getparent()
    children = parent.getchildren()
    total = children.__len__()
    for i in range(0,total):
        if(i in seq_list):
            rslt.append({i:children[i]})
        else:
            pass
    return(rslt)

    


def allSiblings(node,include_self=1):
    info = etree_siblings_info(node)
    seq = info['seq']
    children = info['siblings']
    if(include_self):
        pass
    else:
        children.pop(seq)
    return(children)





#############################


def etree_get_ancestor(node,previous):
    ances = node.getparent()
    for i in range(1,previous):
        ances = ances.getparent()
    return(ances)



#get_json
def bytes_to_json(resp_body_bytes):
    js = resp_body_bytes.decode('utf-8')
    js = json.loads(js)
    return(js)





def encode_disposition_dict(disposition):
    return(head.concat_http_headers_and_body(disposition['headers'],disposition['body']))

def decode_disposition_text(disposition_text,ordered=1):
    disp = head.split_http_headers_and_body(disposition_text)
    disp_head_dict = head.decode_http_headers(disp['headers'])
    disp_head_body = disp['body']
    disp['headers'] = disp_head_dict
    disp['body'] = disp_head_body
    return(disp)

def decode_multipart_text(multipart_text):
    # dont use same boundary when embeded!!!
    arrs = multipart_text.split('\r\n')
    ct = head.decode_one_http_head('Content-Type','; ',arrs[0],1)
    for key in ct:
        v=ct[key]
        if(v[0] == 'boundary'):
            boundary = v[1]
            break
    multipart_text = multipart_text.rstrip('\n')
    multipart_text = multipart_text.rstrip('\r')
    real_boundary = ''.join(('--',boundary))
    end = ''.join((real_boundary,'--'))
    arrs = multipart_text.split(real_boundary)
    rslt = {}
    rslt['headers'] = {}
    rslt['headers'][0] = ct
    disp_texts = {}
    rslt['body'] = {}
    for i in range(1,arrs.__len__()-1):
        rslt['body'][i-1] = {}
        recursive = 0
        disp_texts[i] = arrs[i].lstrip('\r').lstrip('\n')
        disp_texts[i] = disp_texts[i].rstrip('\n').rstrip('\r')
        ct = decode_disposition_text(disp_texts[i])
        for j in range(0,ct['headers'].__len__()):
            head = ct['headers'][j]
            if(head['name'] == 'Content-Type'):
                for key in head:
                    if(head[key][0]==''):
                        if('multipart' in head[key][1]):
                            recursive = 1
        if(recursive == 1):
            rslt['body'][i-1] = decode_multipart_text(head.http_remove_first_head(disp_texts[i]))
        else:
            rslt['body'][i-1] = ct
    return(rslt)            


def encode_multipart_dict(boundary,dispositions,multitipary_header_dict,with_multitipary_header=1):
    '''disp_texts = {}
    disp_texts[0] = 'Content-Disposition: form-data; name="submit-name"\r\nSally'
    disp_texts[1] = 'Content-Disposition: form-data; name="files"\r\nContent-Type: multipart/mixed; boundary=BbC04y\r\n--BbC04y\r\nContent-Disposition: file; filename="essay.txt"\r\nContent-Type: text/plain\r\nplain_text_1\r\n--BbC04y\r\nContent-Disposition: file; filename="essay.txt"\r\nContent-Type: text/plain\r\nplain_text_2\r\n--BbC04y--'
    dispositions = {}
    for i in range(0,disp_texts.__len__()):
        dispositions[i] = decode_disposition_text(disp_texts[i])
    multipart_text = encode_multipart_dict(boundary,dispositions,multitipary_header_dict,with_multitipary_header=1):'''
    real_boundary = ''.join(('--',boundary))
    end = ''.join(('--',boundary,'--'))
    if(with_multitipary_header):
        body = head.encode_one_http_head(multitipary_header_dict,multitipary_header_dict['name'],http_get_splitor_via_headname(multitipary_header_dict['name']),include_head=1)
        body = ''.join((body,'\r\n'))
    else:
        body = ''
    for i in range(0,dispositions.__len__()):
        body = ''.join((body,real_boundary))
        body = ''.join((body,'\r\n'))
        body = ''.join((body,encode_disposition_dict(dispositions[i])))
        body = ''.join((body,'\r\n'))
    body = ''.join(((body),end))
    body = ''.join(((body),'\r\n'))
    return(body)


def findall_jscript_from_resp_body(body,output_file):
    regex_Script = re.compile('<script(.*?)>(.*?)</script>',re.DOTALL)
    regex_Src = re.compile('src=')
    scripts = regex_Script.findall(body.decode('utf-8','ignore'))
    beau_Scripts = {}
    remote_Scripts_TU = {}
    len = scripts.__len__();
    fd = open(output_file,'w+')
    for i in range (0,len):
        beau_Scripts[i+1] = jsbeautifier.beautify(scripts[i][1])
        fd.write('\n//-----{0}------#\n'.format(i+1))
        remote_Scripts_TU[i+1] = scripts[i][0]
        if(regex_Src.search(remote_Scripts_TU[i+1]) == None):
            fd.write('\nlocal_type_:\n{0}\n'.format(remote_Scripts_TU[i+1]))
            fd.write(beau_Scripts[i+1])
            fd.write('\n')
        else:
            fd.write('\nremote_type_src:\n{0}\n'.format(remote_Scripts_TU[i+1]))
        fd.write('\n//-----{0}------#\n'.format(i+1))
    fd.close()
    return((beau_Scripts,remote_Scripts_TU))
    
    
def build_body_string_from_kvlist(KL,KV):
    body = {}
    len = KL.__len__()
    for i in range(0,len):
        body[KL[i]] = KV[i]
    return(urllib.parse.urlencode(body))
    
def decompress_resp_body(resp_body_bytes,resp_or_resp_head):
    if(resp_or_resp_head == None):
        print('----No Resp Received----')
        return(b'')
    else:
        pass
    if(type(resp_or_resp_head) == type([])):
        resp_head = resp_or_resp_head
        ce = head.select_headers_via_key_from_tuple_list(resp_head,'Content-Encoding')
        ce_method = ce[0][1]
    else:
        resp = resp_or_resp_head
        ce_method = resp.getheader('Content-Encoding')
    cond_gzip = (ce_method== 'gzip')
    cond_compress = (ce_method== 'compress')
    cond_deflate = (ce_method== 'deflate')
    cond_identity = (ce_method== 'identity')
    cond_br = (ce_method== 'br')
    if(cond_gzip):
        resp_body_bytes = gzip.decompress(resp_body_bytes)
    elif(cond_compress):
        print('''A format using the Lempel-Ziv-Welch (LZW) algorithm. The value name was taken from the UNIX compress program, which implemented this algorithm.
Like the compress program, which has disappeared from most UNIX distributions, this content-encoding is used by almost no browsers today, partly because of a patent issue (which expired in 2003)''')
        resp_body_bytes = resp_body_bytes
    elif(cond_deflate):
        resp_body_bytes = zlib.decompress(resp_body_bytes)
    elif(cond_identity):
        resp_body_bytes = resp_body_bytes
    elif(cond_br):
        resp_body_bytes = brotli.decompress(resp_body_bytes)
    else:
        resp_body_bytes = resp_body_bytes
    return(resp_body_bytes)
    
def handle_req_body_via_content_type(content_type_head_str,req_body):
    head_dict = head.decode_one_http_head('Content-Type',';',content_type_head_str,ordered=0)
    data_type = head_dict['']
    if('charset' in head_dict):
        charset = head_dict['charset']
    else:
        charset = 'utf-8'
    if('application/json' == data_type):
        if(type(req_body) == type({})):
            req_body = json.dumps(req_body).encode(charset)
        else:
            req_body = req_body
        return(req_body)
    elif('application/x-www-form-urlencoded' == data_type):
        req_body = url_tool.urldecode(req_body)
        return(req_body)
    else:
        return(req_body)

#---------------------
def decode_transfer_encoding_chunked_via_resp(resp):
    pass

def encode_data_bytes_to_transfer_encoding_chunked(data_bytes,slice_sec_list,trailer):
    pass

#-----------------------
def decode_resp_body_bytes(info_container):
    tmp = head.get_content_type_from_resp(info_container['resp'])
    charset = tmp['charset']
    data_type = tmp['data_type']
    html_text = info_container['resp_body_bytes'].decode(charset)
    if('application/json' == data_type.lower):
        js = json.loads(html_text)
        return(js)
    elif('application/x-www-form-urlencoded' == data_type):
        req_body = url_tool.urldecode(html_text)
        return(req_body)
    elif('text/css' == data_type):
        return(html_text)
    else:
        return(html_text)

#
def decode_src(src):
    arr = src.split(',')
    data_scheme = arr[0]
    data = arr[1]
    supported_scheme = [
        'data:'
        'data:text/plain',
        'data:text/html',
        'data:text/html;base64',
        'data:text/css',
        'data:text/css;base64',
        'data:text/JavaScript',
        'data:text/javascript;base64',
        'data:image/gif;base64',
        'data:image/png;base64',
        'data:image/jpeg;base64',
        'data:image/x-icon;base64'
    ]
    index = supported_scheme.__len__()
    for i in range(0,supported_scheme.__len__()):
        if(data_scheme.lower() == supported_scheme[i].lower()):
            index = i
        else:
            pass
    if(index == supported_scheme.__len__()):
        return(src)
    else:
        pass
    data_scheme = supported_scheme[index]
    tmp = data_scheme.split(':')
    head = tmp[0]
    tail = tmp[1]
    rslt = {'type':'','suffix':'','codec':''}
    if(tail==''):
        rslt['type'] = 'text'
        rslt['suffix'] = 'plain'
    else:
        tmp = tail.split(';')
        if(tmp.__len__()==1):
            pass
        else:
            rslt['codec'] = tmp[1]
        tmp = tmp[0].split('/')
        rslt['type'] = tmp[0]
        rslt['suffix'] = tmp[1]
        if(rslt['codec'] == 'base64'):
            rslt['data'] = base64.b64decode(data)
        else:
            rslt['data'] = data
    return(rslt)










#form

def get_form_url(etree_form,url):
    '''
    '''
    dirname,basename = os.path.split(url)
    action_dirname,action_basename = os.path.split(etree_form.attrib['action'])
    if(action_dirname == '.'):
        return(dirname+'/'+action_basename)
    else:
        return(etree_form.attrib['action'])



def get_inputs_from_form(form):
    eles = nvbody.get_eles_via_xpath(form,'//input')
    eles_len = eles.__len__()    
    query_tl = []
    for i in range(0,eles_len):
        ele = eles[i]
        type = ele.attrib['type']
        if(type == 'text'):
            name = ele.attrib['name']
            value = kwargs[name]
            query_tl.append((name,value))
        elif(type == 'password'):
            name = ele.attrib['name']
            value = kwargs[name]
            query_tl.append((name,value))
        elif(type == 'submit'):
            try:
                name = ele.attrib['name']
                value = kwargs[name]
                query_tl.append((name,value))
            except:
                print(ele.attrib)
            else:
                pass
        elif(type == 'hidden'):
            name = ele.attrib['name']
            value = ele.attrib['value']
            query_tl.append((name,value))
        else:
            pass
    inputs = query_tl
    return(inputs)


def get_form_inputs(ic,**kwargs):
    '''
    '''
    root = nvbody.get_etree_root(ic)
    forms = nvbody.get_eles_via_xpath(root,'//form')
    if('which' in kwargs):
        which = kwargs['which']
        form = forms[which]
        return(get_inputs_from_form(form))
    elif('some' in kwargs):
        some = kwargs['some']
        rslt = []
        for i in range(0,some.__len__()):
            form = forms[some[i]]
            rslt.append(get_inputs_from_form(form))
        return(rslt)
    else:
        rslt = []
        for i in range(0,forms.__len__()):
            form = forms[i]
            rslt.append(get_inputs_from_form(form))
        return(rslt)


def build_query_str(inputs_tupleList,**kwargs):
    '''
    '''
    inputs = inputs_tupleList
    query_str = ''
    for i in range(0,inputs.__len__()):
        k = inputs[i][0]
        v = inputs[i][1]
        #此处没有问题，发送form时，需要urlencode
        s = nvurl.urlencode({k:v})
        query_str = query_str + '&' + s
    query_str = query_str.lstrip('&')
    return(query_str)



