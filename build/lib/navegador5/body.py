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

##
def etree_is_leaf_node(node):
    if(node.getchildren().__len__() == 0):
        return(True)
    else:
        return(False)


def etree_get_text(ele):
    it = ele.itertext()
    texts = list(it)
    text = ''
    for i in range(0,texts.__len__()):
        text = text + texts[i]
    return(text)


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




def etree_siblings_info(node):
    parent = node.getparent()
    children = parent.getchildren()
    total = children.__len__()
    for i in range(0,total):
        if(node == children[i]):
            curr_seq = i
        else:
            pass
    return({'total':total,'seq':curr_seq,'parent':parent,'silbings':children})

def etree_get_sibling(node,which,backwards=1):
    parent = node.getparent()
    children = parent.getchildren()
    total = children.__len__()
    for i in range(0,total):
        if(node == children[i]):
            curr_seq = i
        else:
            pass
    if(backwords):
        seq = curr_seq - which
    else:
        seq = curr_seq + which
    if((seq <0) | (seq > (total - 1))):
        return(None)
    else:
        return(children[seq])



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

