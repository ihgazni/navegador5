# Navegador web

import http.client
import urllib.parse
import time
import operator
from navegador5 import url_tool
from navegador5 import shell_cmd
from navegador5 import head
from navegador5 import body
from navegador5.cookie import cookie

def new_info_container():
    info_template = {
        'resp':None,
        'resp_head': [], 
        'resp_body_bytes': None, 
        'req_head': None, 
        'req_body': None, 
        'method':None,
        'url': None, 
        'from_url':None,
        'step': 0, 
        'conn': None,
        'auto_update_cookie':0,
        'auto_redirected':0
    }
    return(info_template)

def new_records_container():
    records_template = {
        'urls':{},
        'referers':{},
        'steps':{}
    }
    return(records_template)


def connection(url_scheme,url_Netloc,**kwargs):
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port =None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 30
    if(url_scheme == 'http'):
        if(port==None):
            port = 80 
        else:
            pass
        conn = http.client.HTTPConnection(url_Netloc,port,timeout)
    else:
        if(port==None):
            port = 443 
        else:
            pass
        conn = http.client.HTTPSConnection(url_Netloc,port,None,None,timeout)
    return(conn)

def stepping_req(conn,method,url_path,**kwargs):
    '''
        refer to https://docs.python.org/3/library/http.client.html
        If headers contains neither Content-Length nor Transfer-Encoding, but there is a request body, 
        one of those header fields will be added automatically. If body is None, 
        the Content-Length header is set to 0 for methods that expect a body (PUT, POST, and PATCH). 
        If body is a string or a bytes-like object that is not also a file, the Content-Length header is set to its length. 
        Any other type of body (files and iterables in general) will be chunk-encoded, 
        and the Transfer-Encoding header will automatically be set instead of Content-Length.
        The encode_chunked argument is only relevant if Transfer-Encoding is specified in headers. 
        If encode_chunked is False, the HTTPConnection object assumes that all encoding is handled by the calling code. 
        If it is True, the body will be chunk-encoded.
        Changed in version 3.6: If neither Content-Length nor Transfer-Encoding are set in headers, 
        file and iterable body objects are now chunk-encoded. The encode_chunked argument was added. 
        No attempt is made to determine the Content-Length for file objects.
    '''
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if('req_head' in kwargs):
        req_head = kwargs['req_head']
    else:
        req_head = None
    if(type({}) == type(req_head)):
        req_head_dict = req_head
    else:
        req_head_dict = None
    if(type('') == type(req_head)):
        req_head_str = req_head
    else:
        req_head_str = None
    if(req_head_str==None):
        if(req_head_dict==None):
            req_head_dict = {}
        else:
            req_head_dict = req_head_dict
    else:
        req_head_dict = head.build_headers_dict_from_str(req_head_str,'\n')
    #body is string or bytes
    if('req_body' in kwargs):
        req_body = kwargs['req_body']
    else:
        req_body = None
    if(method == "GET"):
        if(type(req_body)==type({})):
            req_body = url_tool.urlencode(req_body)
            url_path = ''.join((url_path,"?",req_body))
    if(method == "POST"):
        if(type(req_body)==type({})):
            req_body = url_tool.urlencode(req_body)
    try:
        conn.request(method,url_path,headers=req_head_dict,body=req_body)
    except Exception as e:
        #to avoid socket.gaierror: [Errno -2] Name or service not known
        print(e)
    else:
        pass
    return(conn)

def linux_check_tcp_state(conn):
    LA  = ''.join((conn.sock.getsockname()[0],':',str(conn.sock.getsockname()[1])))
    FA = ''.join((conn.sock.getpeername()[0],':',str(conn.sock.getpeername()[1])))
    egrep_RE_string = ''.join((LA,'[ ]+',FA))
    shell_CMDs = {}
    shell_CMDs[1] = 'netstat -n'
    shell_CMDs[2] = ''.join(('egrep ','"',egrep_RE_string,'"'))
    shell_CMDs[3] = "awk {'print $6'}"
    state = shell_cmd.pipe_shell_cmds(shell_CMDs)[0].decode().strip('\n').strip(' ')
    return(state)

def linux_manual_close_conn(conn,keepalive_timeout):
    time.sleep(keepalive_timeout)
    r_TCP_state = self.linux_check_tcp_state(conn)
    print(r_TCP_state)
    if(r_TCP_state=='ESTABLISHED'):
        pass
    else:
        print('TCP STATE {0} ,IMPLICIT CONN RESP MODE, CLOSE CONN'.format(r_TCP_state))
        conn.close()

####
class RespError(Exception):
    pass

class RespHeadError(Exception):
    pass

class RespBodyError(Exception):
    pass
####

def stepping_resp(conn,explicit_keepalive=0):
    try:
        resp = conn.getresponse()
    except Exception as e:
        print("----resp Exception-----")
        print("Exception: ")
        print(e)
        print("----resp Exception-----")
        #return((conn,[],None,None))
        raise RespError()
    else:
        pass
    try:
        resp_head = resp.getheaders()
    except Exception as e:
        print("----resp_head Exception-----")
        print("Exception: ")
        print(e)
        print("----resp_head Exception-----")
        #return((conn,[],None,None))
        raise RespHeadError()
    else:
        pass
    try:
        resp_body_bytes = resp.read()
    except Exception as e:
        print("----resp_body Exception-----")
        print("Exception: ")
        print(e)
        print("resp_head: ")
        print(resp_head)
        #resp_body_bytes = None
        print("resp_body_bytes: ")
        print(resp_body_bytes)
        print("----resp_body Exception-----")
        raise RespBodyError()
    else:
        pass
    #
    secarino_1 = head.name_value_exist_in_headers(resp_head,'Connection','Keep-Alive')
    secarino_2 = head.name_value_exist_in_headers(resp_head,'Connection','keep-alive')
    #
    if((secarino_1 == 0)&(secarino_2 == 0)):
        # no Connection exist
        rkeepalive = 0
    elif((secarino_1 == 1)|(secarino_2 == 1)):
        # Connection = Keep-Alive
        rkeepalive = 1
    else:
        # Connection = close
        rkeepalive = -1
    if(rkeepalive==0):
        if(explicit_keepalive==0):
            pass
        else:
            conn.close()
    elif(rkeepalive==-1):
        conn.close()
    else:
        pass
    return((conn,resp_head,resp_body_bytes,resp))


def obseleted_walkon(info_container,**kwargs):
    '''by default auto_update_cookie enabled'''
    step = info_container['step']
    ####
    #from_url = info_container['from_url']
    ####
    url = info_container['url']
    method = info_container['method']
    conn = info_container['conn']
    req_head = info_container['req_head']
    #body is string or bytes
    req_body = info_container['req_body']
    if(info_container['method'] == 'GET'):
        try:
            del info_container['req_head']['Content-Type']
            del info_container['req_head']['Content-Length']
        except:
            pass
        else:
            pass
        info_container['req_body'] = None
    else:
        pass
    if('save_scripts' in kwargs):
        save_scripts = kwargs['save_scripts']
    else:
        save_scripts = 0
    if('explicit_keepalive' in kwargs):
        explicit_keepalive = kwargs['explicit_keepalive']
    else:
        explicit_keepalive = 0
    url_scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    if('default_port' in kwargs):
        default_port = kwargs['default_port']
    else:
        if('https' in url_scheme):
            default_port = 443
        elif('http' in url_scheme):
            default_port = 80
        else:
            default_port = None
    url_NL_HP = url_tool.parse_url_netloc(url_Netloc,default_port)
    url_host = url_NL_HP[0]
    url_port = url_NL_HP[1]
    url_path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    if('upgrade_records' in kwargs):
        upgrade_records = kwargs['upgrade_records']
    else:
        upgrade_records = 1
    if(upgrade_records):
        if('records_container' in kwargs):
            records_container = kwargs['records_container']
        else:
            records_container = new_records_container()
        records_container['steps'][step] = step
        records_container['urls'][step] = url
        if('Referer' in info_container['req_head']):
            records_container['referers'][step] = info_container['req_head']['Referer']
    else:
        pass
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port = None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 30
    if(step == 0):
        conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
    else:
        if(conn.sock == None):
            conn.close()
            conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
        else:
            if(conn==None):
                conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
            else:
                conn = conn
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if(url_Query == ''):
        conn = stepping_req(conn,method,url_path,req_head=req_head,req_body=req_body)
    else:
        conn = stepping_req(conn,method,url_path+'?'+url_Query,req_head=req_head,req_body=req_body)
    conn,resp_head,resp_body_bytes,resp = stepping_resp(conn,explicit_keepalive=explicit_keepalive)
    resp_body_bytes = body.decompress_resp_body(resp_body_bytes,resp)
    if(save_scripts):
        body.findall_jscript_from_resp_body(resp_body_bytes,'s{0}'.format(step))
    else:
        pass
    step = step + 1
    info_container['step'] = step
    info_container['conn'] = conn
    info_container['resp_head'] = resp_head
    info_container['resp_body_bytes'] = resp_body_bytes
    info_container['resp'] = resp
    #--------------------------------加入cookie处理-------
    if('auto_update_cookie' in kwargs):
        auto_update_cookie = kwargs['auto_update_cookie']
    else:
        auto_update_cookie = 1
    if(auto_update_cookie):
        #from_url = url
        if('to_url' in kwargs):
            to_url = kwargs['to_url']
        else:
            to_url = from_url
        ##
        ##print("---------")
        ##print(req_head)
        ##print("---------")
        ##print(resp_head)
        ##print("---------")
        ##print(from_url)
        ##print("---------")
        ##print(to_url)
        ##print("---------")
        ##
        next_req_cookie_dict = cookie.select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url)
        next_req_cookie_str = cookie.cookie_dict_to_str(next_req_cookie_dict,with_head=0)
        ####
        ##print(next_req_cookie_dict)
        ##print("---------")
        ##print(next_req_cookie_str)
        ####
        if(next_req_cookie_str ==""):
            pass
        else:
            ##print("---req_head---")
            ##print(req_head)
            ##print("---req_head_type---")
            ##print(type(req_head))
            if(type(req_head) == type({})):
                req_head['Cookie'] = next_req_cookie_str
            elif(type(req_head) == type('')):
                req_head_dict = head.build_headers_dict_from_str(req_head)
                req_head_dict['Cookie'] = next_req_cookie_str
                req_head = head.build_headers_str_from_dict(req_head_dict)
            else:
                pass
        info_container['req_head'] = req_head
        info_container['auto_update_cookie'] = 1
    else:
        info_container['auto_update_cookie'] = 0
    #--------------------------------加入cookie处理-------
    return(info_container)




def walkon(info_container,**kwargs):
    '''by default auto_update_cookie enabled'''
    #try:
    #    print(info_container['req_head']['Cookie'])
    #except:
    #    pass
    #else:
    #    pass
    #print("--------------------------------------")

    step = info_container['step']
    from_url = info_container['from_url']
    url = info_container['url']
    #for the first request
    if(from_url == None):
        from_url = url
    else:
        pass
    to_url = url
    method = info_container['method']
    conn = info_container['conn']
    req_head = info_container['req_head']
    resp_head = info_container['resp_head']
    #--------------------------------加入cookie处理-------
    if('auto_update_cookie' in kwargs):
        auto_update_cookie = kwargs['auto_update_cookie']
    else:
        auto_update_cookie = 1
    if(auto_update_cookie):
        next_req_cookie_dict = cookie.select_valid_cookies_from_resp(req_head,resp_head,from_url,to_url)
        next_req_cookie_str = cookie.cookie_dict_to_str(next_req_cookie_dict,with_head=0)
        if(next_req_cookie_str ==""):
            pass
        else:
            if(type(req_head) == type({})):
                req_head['Cookie'] = next_req_cookie_str
            elif(type(req_head) == type('')):
                req_head_dict = head.build_headers_dict_from_str(req_head)
                req_head_dict['Cookie'] = next_req_cookie_str
                req_head = head.build_headers_str_from_dict(req_head_dict)
            else:
                pass
        info_container['req_head'] = req_head
        info_container['auto_update_cookie'] = 1
    else:
        info_container['auto_update_cookie'] = 0
    #--------------------------------加入cookie处理-------
    #try:
    #    print(info_container['req_head']['Cookie'])
    #except:
    #    pass
    #else:
    #    pass
    #
    #body is string or bytes
    req_body = info_container['req_body']
    if(info_container['method'] == 'GET'):
        try:
            del info_container['req_head']['Content-Type']
            del info_container['req_head']['Content-Length']
        except:
            pass
        else:
            pass
        info_container['req_body'] = None
    else:
        pass
    if('save_scripts' in kwargs):
        save_scripts = kwargs['save_scripts']
    else:
        save_scripts = 0
    if('explicit_keepalive' in kwargs):
        explicit_keepalive = kwargs['explicit_keepalive']
    else:
        explicit_keepalive = 0
    url_scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    if('default_port' in kwargs):
        default_port = kwargs['default_port']
    else:
        if('https' in url_scheme):
            default_port = 443
        elif('http' in url_scheme):
            default_port = 80
        else:
            default_port = None
    url_NL_HP = url_tool.parse_url_netloc(url_Netloc,default_port)
    url_host = url_NL_HP[0]
    url_port = url_NL_HP[1]
    url_path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    if('upgrade_records' in kwargs):
        upgrade_records = kwargs['upgrade_records']
    else:
        upgrade_records = 1
    if(upgrade_records):
        if('records_container' in kwargs):
            records_container = kwargs['records_container']
        else:
            records_container = new_records_container()
        records_container['steps'][step] = step
        records_container['urls'][step] = url
        if('Referer' in info_container['req_head']):
            records_container['referers'][step] = info_container['req_head']['Referer']
    else:
        pass
    if('port' in kwargs):
        port = kwargs['port']
    else:
        port = None
    if('timeout' in kwargs):
        timeout = kwargs['timeout']
    else:
        timeout = 30
    if(step == 0):
        conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
    else:
        if(conn.sock == None):
            conn.close()
            conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
        else:
            if(conn==None):
                conn = connection(url_scheme,url_Netloc,port=port,timeout=timeout)
            else:
                conn = conn
    #encode_chunked only supportted in python3.6
    if('encode_chunked' in kwargs):
        encode_chunked = kwargs['encode_chunked']
    else:
        encode_chunked = False
    if(url_Query == ''):
        conn = stepping_req(conn,method,url_path,req_head=req_head,req_body=req_body)
    else:
        conn = stepping_req(conn,method,url_path+'?'+url_Query,req_head=req_head,req_body=req_body)
    conn,resp_head,resp_body_bytes,resp = stepping_resp(conn,explicit_keepalive=explicit_keepalive)
    resp_body_bytes = body.decompress_resp_body(resp_body_bytes,resp)
    if(save_scripts):
        body.findall_jscript_from_resp_body(resp_body_bytes,'s{0}'.format(step))
    else:
        pass
    step = step + 1
    info_container['step'] = step
    info_container['conn'] = conn
    info_container['resp_head'] = resp_head
    info_container['resp_body_bytes'] = resp_body_bytes
    info_container['resp'] = resp
    info_container['from_url'] = url
    return(info_container)


















#-----------dont put this func in walkon, coz recursive
def auto_redireced(info_container,records_container,max_redirects=10):
    #------------------auto redirect-----------------------
    count = 0
    while(count<max_redirects):
        redirect_url = head.get_abs_redirect_url_from_resp(info_container['resp'],info_container['url'])
        if(redirect_url):
            info_container['url'] = redirect_url
            info_container = walkon(info_container,records_container=records_container)
        else:
            break
        count = count + 1
    info_container['auto_redirected'] = 1
    return(info_container)
    

