import operator
import re
from navegador5 import url_tool

#resp 
#resp_head = resp.getheaders()  tuple_list
#resp_body_bytes = resp.read()

def split_one_header_str_to_tuple(header_String):
    regex_Header_String = re.compile('(.*?): (.*)')
    m = regex_Header_String.search(header_String)
    return((m.group(1),m.group(2)))

def split_http_headers_and_body(http_all):
    rslt = {'headers':'','body':''}
    arrs_rn = http_all.split('\r\n\r\n')
    arrs = http_all.split('\r\n')     
    if(arrs_rn.__len__()>1):
        rslt['headers'] = arrs_rn[0]
        rslt['body'] = arrs_rn[1]
        for i in range(1,arrs_rn.__len__()):
            rslt['body'] = ''.join((rslt['body'],arrs_rn[i],'\r\n\r\n'))
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
    else:
        regex_rstrip_one = re.compile('(.*)\r\n')
        regex_colon = re.compile('^[A-Z][a-zA-Z\-]+: ')
        label = -1
        for i in range(0,arrs.__len__()):
            if(regex_colon.search(arrs[i])):
                pass
            else:
                label = i
                break
        rslt['headers'] = ''
        rslt['body'] = ''
        for i in range(0,label):
            rslt['headers'] = ''.join((rslt['headers'],arrs[i],'\r\n'))
        rslt['headers'] = rslt['headers'].rstrip('\n')
        rslt['headers'] = rslt['headers'].rstrip('\r')
        for i in range(label,arrs.__len__()):
            rslt['body'] = ''.join((rslt['body'],arrs[i],'\r\n'))
        rslt['body'] = rslt['body'].rstrip('\n')
        rslt['body'] = rslt['body'].rstrip('\r')
        if(label == -1):
            rslt['headers'] = http_all
            rslt['body'] = None
    return(rslt)

def concat_http_headers_and_body(headers_dict,body_text):
    head_text = encode_http_headers(headers_dict)
    sp = '\r\n\r\n'
    rslt = ''.join((head_text,sp,body_text))
    return(rslt)

def decode_one_http_head(head_name,splitor,body_text,ordered=1):
    s_rep = ''.join((splitor,' '))
    body_text = body_text.replace(s_rep,splitor)
    #use ordered as possible as you can 
    regex = re.compile(''.join((head_name,': ')))
    m = regex.search(body_text)
    if(m):
        len = ''.join((head_name,': ')).__len__()
        body_text = body_text[len:]
    else:
        pass
    regex_colon = re.compile('^([A-Z][a-zA-Z\-]+): ')
    m = regex_colon.search(body_text)
    if(m):
        head_name = m.group(1)
        len = ''.join((head_name,': ')).__len__()
        body_text = body_text[len:]
    else:
        pass
    rslt = {}
    arrs = body_text.split(splitor)
    for i in range(0,arrs.__len__()):
        each = arrs[i]
        regex = re.compile('(.*?)=(.*)')
        m = regex.search(each)
        if(m):
            kv = [m.group(1),m.group(2)]
        else:
            kv = [each]
        key =kv[0]
        if(kv.__len__()==1):
            value = None
            if(ordered):
                rslt['name'] = head_name
                rslt[i] = ('',key)
            else:
                rslt[' '] = head_name
                rslt[''] = key
        else:
            value = kv[1]
            if(ordered):
                rslt['name'] = head_name 
                rslt[i] = (key,value)
            else:
                rslt[' '] = head_name
                rslt[key] = value
    return(rslt)

def encode_one_http_head(body_dict,head_name,splitor,include_head=0):
    body = ''
    if(include_head):
        rslt = ''.join((head_name,': '))
    else:
        rslt = ''
    ordered = 0
    for key in body_dict:
        if(type(body_dict[key]) == type(())):
            ordered = 1
            break
    if(ordered):
        for key in body_dict:
            if(type(key)==type(0)):
                kv = body_dict[key]
                k = kv[0]
                v = kv[1]
                if(k==''):
                    body = ''.join((body,splitor,v))
                else:
                    body = ''.join((body,splitor,k,'=',v))
    else:
        for key in body_dict:
            if(type(key)==type(0)):
                k = key
                v = body_dict[key]
                if(k==''):
                    body = ''.join((body,splitor,v))
                else:
                    body = ''.join((body,splitor,k,'=',v))
    len = splitor.__len__()                
    body = body[len:]
    rslt = ''.join((rslt,body))
    return(rslt)

def decode_http_headers(headers_text,ordered=1):
    rslt = {}
    arrs = headers_text.split('\r\n')
    for i in range(0,arrs.__len__()):
        one_http_header = arrs[i].split(': ')
        header_name = one_http_header[0]
        header_body = one_http_header[1]
        if(', ' in header_body):
            splitor = ' ,'
        elif(',' in header_body):
            splitor = ','
        elif(' ;' in header_body):
            splitor = '; '
        else:
            splitor = '; '
        if(ordered):
            rslt[i] = decode_one_http_head(header_name,splitor,header_body,ordered)
        else:
            rslt[header_name] = decode_one_http_head(header_name,splitor,header_body,ordered)
    return(rslt)

def encode_http_headers(headers_dict):
    rslt = ''
    for i in range(0,headers_dict.__len__() - 1):
        splitor = http_get_splitor_via_headname(headers_dict[i]['name'])
        text = encode_one_http_head(headers_dict[i],headers_dict[i]['name'],splitor,include_head=1)
        rslt = ''.join((rslt,text,'\r\n'))
    i = headers_dict.__len__() - 1
    splitor = http_get_splitor_via_headname(headers_dict[i]['name'])
    text = encode_one_http_head(headers_dict[i],headers_dict[i]['name'],splitor,include_head=1)
    rslt = ''.join((rslt,text))
    return(rslt)

def http_get_splitor_via_headname(head_name):
    const_http_header_splitor_dict = {
        'Accept':", ",
        'Accept-Encoding':", ",
        'Content-Disposition':"; ",
        'Content-Type':"; ",
        'Cookie':"; ",
        'X-UA-Compatible':','
    }
    if(head_name in const_http_header_splitor_dict):
        return(const_http_header_splitor_dict[head_name])
    else:
        return('; ')

def http_remove_first_head(disp_text):
    rslt =''
    arrs = http_all.split('\r\n')
    for i in range(1,arrs.__len__()):
        rslt = ''.join((rslt,'\r\n',arrs[i]))
    return(rslt.lstrip('\r').lstrip('\n'))

###################################3
def build_headers_dict_from_str(head_str,SP='\r\n'):
    '''
    head_str = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\nAccept-Encoding: gzip,deflate,sdch\nAccept-Language: en;q=1.0, zh-CN;q=0.8'
    '''
    headers = {}
    regex_H = re.compile('(.*): (.*)')
    sp_HS = head_str.split(SP)
    for i in range(0,sp_HS.__len__()):
        m = regex_H.search(sp_HS[i])
        HN = m.group(1)
        HV = m.group(2)
        headers[HN] = HV
    return(headers)

def build_headers_tuple_list_from_str(head_str,SP='\r\n'):
    '''
    head_str = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\nAccept-Encoding: gzip,deflate,sdch\nAccept-Language: en;q=1.0, zh-CN;q=0.8'
    '''
    headers = []
    regex_H = re.compile('(.*): (.*)')
    sp_HS = head_str.split(SP)
    for i in range(0,sp_HS.__len__()):
        m = regex_H.search(sp_HS[i])
        HN = m.group(1)
        HV = m.group(2)
        headers.append((HN,HV))
    return(headers)

def build_headers_str_from_dict(head_dict):
    head_str =''
    for key in head_dict:
        head_str = ''.join((head_str,key,': ',head_dict[key],'\r\n'))
    head_str.rstrip('\n')
    head_str.rstrip('\r')
    return(head_str)

def build_headers_str_from_tuple_list(head_tuple_list):
    head_str =''
    for i in range(0,head_tuple_list.__len__()):
        temp = head_tuple_list[i]
        key = temp[0]
        value = temp[1]
        head_str = ''.join((head_str,key,': ',value,'\r\n'))
    head_str.rstrip('\n')
    head_str.rstrip('\r')
    return(head_str)



def http_remove_head_from_head_str(head_name,head_str,keep_order=0):
    if(keep_order):
        head_tuple_list = build_headers_tuple_list_from_str(head_str)
        head_str =''
        for i in range(0,head_tuple_list.__len__()):
            temp = head_tuple_list[i]
            key = temp[0]
            value = temp[1]
            if(key == head_name):
                pass
            else:
                head_str = ''.join((head_str,key,': ',value,'\r\n'))
        head_str.rstrip('\n')
        head_str.rstrip('\r')
    else:
        head_dict = build_headers_dict_from_str(head_str)
        del head_dict[head_name]
        head_str = build_headers_str_from_dict(head_dict)
    return(head_str)



def expand_headers_dict_via_head_string_list(Cheaders,ex_String_List):
    new_Cheaders = {}
    for each in Cheaders:
        new_Cheaders[each] = Cheaders[each]
    regex_H = re.compile('(.*): (.*)')
    for each in ex_String_List:
        m = regex_H = re.compile('(.*): (.*)')
        new_Cheaders[m.group(1)] = m.group(2)
    return(new_Cheaders)

    
    

#############
def with_quality_head_str_to_tuple_list(Accept_text,name,sp=','):
    '''
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept
        Accept: <MIME_type>/<MIME_subtype>
        Accept: <MIME_type>/*
        Accept: */*
        Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8
        Accept_text = 'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'
        accept_head_str_to_dict(Accept_text)
        
        apply to name :  Accept ,Accept-Charset,Accept-Encoding,Accept-Language,Accept-Ranges,Keep-Alive
    '''
    s_rep = ''.join((sp,' '))
    Accept_text = Accept_text.replace(s_rep,sp)
    Accept_dict = decode_one_http_head(name,sp,Accept_text,ordered=1)
    name_list = []
    qualisty_list = []
    seq = 0
    for i in range(0,Accept_dict.__len__()-1):
        kv = Accept_dict[i]
        k = Accept_dict[i][0]
        v = Accept_dict[i][1]
        if(k == ''):
            name_list.append(v)
            qualisty_list.append(1.0)
        else:
            key = k.rstrip('q').rstrip(';')
            name_list.append(key)
            qualisty_list.append(float(v))
    pn_list = {}
    for i in range(0,qualisty_list.__len__()):
        pn_list[name_list[i]] = qualisty_list[i]
    new_pn_list = sorted(pn_list.items(), key=operator.itemgetter(1),reverse=True)
    return(new_pn_list)


def with_quality_head_tuple_list_to_str(head_tuple_list,name,sp=',',explicit=0):
    head = ''.join((name,': '))
    for i in range(0,head_tuple_list.__len__()):
        t = head_tuple_list[i][0]
        q = head_tuple_list[i][1]
        if((explicit==0) & (q==1.0)):
            tq = ''.join((t,sp,' '))
        else:
            tq = ''.join((t,';','q=',str(q),sp,' '))
        head = ''.join((head,tq))
    head = head.rstrip(' ')
    head = head.rstrip(sp)
    return(head)


def access_control_head_str_to_tuple_list(Accept_text,name):
    '''
        Access-Control-Allow-Credentials
        Access-Control-Allow-Headers
        Access-Control-Allow-Methods
        Access-Control-Allow-Origin
        Access-Control-Expose-Headers
        Access-Control-Max-Age
        Access-Control-Request-Headers
        Access-Control-Request-Method
    '''
    Accept_text = Accept_text.replace(', ',',')
    Accept_dict = decode_one_http_head(name,',',Accept_text,ordered=1)
    name_list = []
    qualisty_list = []
    seq = 0
    for i in range(0,Accept_dict.__len__()-1):
        kv = Accept_dict[i]
        k = Accept_dict[i][0]
        v = Accept_dict[i][1]
        if(k == ''):
            name_list.append(v)
            qualisty_list.append(1.0)
        else:
            key = k.rstrip('q').rstrip(';')
            name_list.append(key)
            qualisty_list.append(float(v))
    pn_list = {}
    for i in range(0,qualisty_list.__len__()):
        pn_list[name_list[i]] = qualisty_list[i]
    new_pn_list = sorted(pn_list.items(), key=operator.itemgetter(1),reverse=True)
    return(new_pn_list)


def access_control_head_tuple_list_to_str(head_tuple_list,name,explicit=0):
    head = ''.join((name,': '))
    for i in range(0,head_tuple_list.__len__()):
        t = head_tuple_list[i][0]
        q = head_tuple_list[i][1]
        if((explicit==0) & (q==1.0)):
            tq = ''.join((t,', '))
        else:
            tq = ''.join((t,';','q=',str(q),', '))
        head = ''.join((head,tq))
    head = head.rstrip(' ')
    head = head.rstrip(',')
    return(head)




def name_value_exist_in_headers(rheaders,header,HV):
    len = rheaders.__len__()
    for i in range(0,len):
        if(rheaders[i][0]==header):
            if(rheaders[i][1]==HV):
                return(1)
            else:
                return(-1)
    return(0)


def select_headers_via_key_from_tuple_list(headers_turple_array,key):
    # 返回的是符合条件的tuple_list
    arr = headers_turple_array
    arr_len = arr.__len__()
    rslt = []
    for i in range(0,arr_len):
        k = arr[i][0]
        v = arr[i][1]
        if(k.upper() == key.upper()):
            temp = (k,v)
            rslt.append(temp)
    return(rslt)
    


def get_resp_headers_vl_dict_from_resp(resp):
    Rheaders_Dict = {}
    keys = resp.info().keys()
    values = resp.info().values()
    for i in range(0,keys.__len__()):
        if(keys[i] in Rheaders_Dict):
            Rheaders_Dict[keys[i]].append(values[i])
        else:
            Rheaders_Dict[keys[i]] = [values[i]]
    return(Rheaders_Dict)

    
def is_mobile_user_agent(Cheaders):
    CUA = Cheaders['User-Agent']
    regex_Mobile_UA = re.compile('applewebkit.*mobile.*|windows.*phone.*mobile.*|msie.*touch.*wpdesktop|android.*mobile.*|android.*applewebkit.*',re.I)
    if(regex_Mobile_UA.search(CUA)):
        return(True)
    else:
        return(False)

def creat_B2I_url(Cheaders,Rerirecto_Url):
    regex_B2I = re.compile('bootstrap')
    if(is_mobile_user_agent(Cheaders)):
        url = regex_B2I.sub('mobile_index',Rerirecto_Url,0)
    else:
        url = regex_B2I.sub('index',Rerirecto_Url,0)
    return(url)
    


def get_content_type_from_resp(resp):
    resp_head_dict = get_resp_headers_vl_dict_from_resp(resp)
    #ct = resp.getheader('Content-Type')
    if('Content-Type' in resp_head_dict):
    #if(ct):
        charset = ['utf-8']
        ct = resp_head_dict['Content-Type']
        for i in range(0,ct.__len__()):
            temp = ct[i].split('; ')
            for j in range(0,temp.__len__()):
                if('/' in temp[j]):
                    data_type = temp[j]
                elif('charset' in temp[j]):
                    t = temp[j].split('=')
                    charset = t[1]
        return({'data_type':data_type,'charset':charset})
    else:
        return(None)


def get_rel_redirect_url_from_resp(resp):
    if(resp.status == 302):
        return(resp.getheader('Location'))
    else:
        return(None)



def get_abs_redirect_url_from_resp(resp,url):
    resp_head_dict = get_resp_headers_vl_dict_from_resp(resp)
    base_url = url_tool.get_base_url(url)
    if('Location' in resp_head_dict):
        loc = resp_head_dict['Location'][0]
        regex = re.compile('^/')
        m = regex.search(loc)
        if(m):
            return(''.join((base_url,loc)))
        else:
            return(loc)
    else:
        return(None)


#-----------------------------------implement cache
def get_cache_control_dict():
    ccd = {}
    ccd['request'] = ['max-age','max-stale','min-fresh','no-cache','no-store','no-transform','only-if-cached']
    ccd['response'] = ['must-revalidate', 'no-cache', 'no-store', 'no-transform', 'public', 'private', 'proxy-revalidate', 'max-age', 's-maxage']
    ccd['extension'] = ['immutable','stale-while-revalidate','stale-if-error']
    return(ccd)

def creat_cache_dir():
    '''
        public
        private-user1
               -user2
               -user3
        
    '''

def handle_cache_control(cache_control_text):
    cache_control_text = cache_control_text.replace(', ',',')
    cache_control_dict = decode_one_http_head('Cache-control',',',cache_control_text,ordered=1)
    for i in range(0,Accept_dict.__len__()-1):
        v = cache_control_dict[i][1]
        if('public' in v):
            print('the response may be cached by any cache')
        elif('private' in v):
            print('A private cache may store the response')
        elif('no-cache' in v):
            print('submit the request to the origin server for validation before releasing a cached copy.')
        elif('only-if-cached' in v):
            print('only wishes to obtain a cached response, and should not contact the origin-server to see if a newer copy exists')
            