import urllib.parse
import os
import re

def get_base_url(url):
    temp = urllib.parse.urlparse(url)
    netloc = temp.netloc
    scheme = temp.scheme
    base_url = ''.join((scheme,'://',netloc))
    return(base_url)

def url_to_dirpath(url):
    netloc = urllib.parse.urlparse(url).netloc
    path = urllib.parse.urlparse(url).path
    dirpath = ''.join((netloc,path))
    if(os.path.exists(dirpath)):
        pass
    else:
        os.makedirs(dirpath)
    return(dirpath)
    

def url_to_fn(url):
    netloc = urllib.parse.urlparse(url).netloc
    path = urllib.parse.urlparse(url).path
    path = path.replace("/","_")
    fn = ''.join((netloc,"__",path,".","html"))
    return(fn)

def parse_url_netloc(url_Netloc,default_Port):
    regex_Netloc = re.compile('(.*):(.*)')
    m = regex_Netloc.search(url_Netloc)
    if(m == None):
        url_Netloc_Host = url_Netloc
        url_Netloc_Port = default_Port
    else:
        url_Netloc_Host = m.group(1)
        url_Netloc_Port = m.group(2)
    return((url_Netloc_Host,url_Netloc_Port))

def url_to_tuple(url):
    url_Scheme = urllib.parse.urlparse(url).scheme
    url_Netloc = urllib.parse.urlparse(url).netloc
    url_Path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    return((url_Scheme,url_Netloc,url_Path,url_Params,url_Query,url_Fragment))


def url_to_dict(url,**kwargs):
    '''
        url = "foo://example.com:8042/over/there?name=ferret#nose"
        url = "http://www.blah.com/some;param1=foo/crazy;param2=bar/path.html"
        url =  "http://www.blah.com/some/crazy/path.html;param1=foo;param2=bar"
    '''
    if("http_default_port" in kwargs):
        http_default_port = kwargs['http_default_port']
    else:
        http_default_port = 80
    if("https_default_port" in kwargs):
        https_default_port = kwargs['https_default_port']
    else:
        https_default_port = 443
    url_Scheme = urllib.parse.urlparse(url).scheme
    if(url_Scheme == 'http'):
        default_Port = http_default_port
    else:
        default_Port = https_default_port
    url_Netloc = urllib.parse.urlparse(url).netloc
    url_NL_HP = parse_url_netloc(url_Netloc,default_Port)
    url_Netloc_Host = url_NL_HP[0]
    url_Netloc_Port = url_NL_HP[1]
    url_Path = urllib.parse.urlparse(url).path
    url_Params = urllib.parse.urlparse(url).params
    url_Query = urllib.parse.urlparse(url).query
    url_Fragment = urllib.parse.urlparse(url).fragment
    rslt = {}
    rslt['scheme'] = url_Scheme
    rslt['netloc'] = url_Netloc
    rslt['host'] = url_Netloc_Host
    rslt['port'] = url_Netloc_Port    
    rslt['path'] = url_Path    
    rslt['params'] = url_Params    
    rslt['query'] = url_Query    
    rslt['fragment'] = url_Fragment    
    return(rslt)

def dict_to_url(url_dict):
    '''scheme://host:port/path?query#fragment
     url = "https://servicegate.suunto.com/UserAuthorityService/?callback=jQuery18108122223665320987_1485771086287&service=Movescount&emailAddress=xxxxxxxx%40163.com&password=xxxxxx&_=1485771109116#a=b&c=d&e=f"
     urllib.parse.urlparse(url)
     <scheme>://<username>:<password>@<host>:<port>/<path>;<parameters>?<query>#<fragment>
     url2 = "http://www.blah.com/some;param1=foo/crazy;param2=bar/path.html"
     >>> urllib.parse.urlparse(url2)
     ParseResult(scheme='http', netloc='www.blah.com', path='/some;param1=foo/crazy;param2=bar/path.html', params='', query='', fragment='')
     urllib.parse.urlparse(url2)
     url3 = "http://www.blah.com/some/crazy/path.html;param1=foo;param2=bar"
    >>> urllib.parse.urlparse(url3)
     ParseResult(scheme='http', netloc='www.blah.com', path='/some/crazy/path.html', params='param1=foo;param2=bar', query='', fragment='')
     params_dict = {'param1': 'foo', 'param2': 'bar'}
     
     servicegate_url_dict = {
        'scheme':"https",
        'netloc':"servicegate.suunto.com",
        'path':"UserAuthorityService",
        'query_dict':{
            'callback': jQuery_get_random_jsonpCallback_name(),
            'emailAddress':"terryinzaghi@163.com",
            'password':"shu6LA",
            '_':jQuery_unix_now(),
            'service':"Movescount"
        }
    }
     '''
    url_dict_template = {
        'scheme':"",
        'sp_scheme_host':"://",
        'host':"",
        'sp_host_port':":",
        'port':{
            'explicit':"",
            'implicit':""
        },
        'netloc':"",
        'sp_netloc_path':"/",
        'path':"",
        'sp_path_params':";",
        'params':"",
        'params_dict':{},
        'sp_params_query':"/?",
        'query':"",
        'query_dict':{},
        'sp_query_fragment':"#",
        'fragment':"",
        'fragment_dict':{},
        'hash':"",
        'hash_dict':{}
    }
    url_dict_template['scheme'] = url_dict['scheme']
    if('sp_scheme_host' in url_dict):
        url_dict_template['sp_scheme_host'] = url_dict['sp_scheme_host']
    if('sp_host_port' in url_dict):
        url_dict_template['sp_host_port'] = url_dict['sp_host_port']
    if('sp_netloc_path' in url_dict):
        url_dict_template['sp_netloc_path'] = url_dict['sp_netloc_path']
    if('sp_path_params' in url_dict):
        url_dict_template['sp_path_params'] = url_dict['sp_path_params']
    if('sp_params_query' in url_dict):
        url_dict_template['sp_params_query'] = url_dict['sp_params_query']
    if('sp_query_fragment' in url_dict):
        url_dict_template['sp_query_fragment'] = url_dict['sp_query_fragment']
    if('netloc' in url_dict):
        url_dict_template['netloc'] = url_dict['netloc']
    elif('host' in url_dict):
        if('port' in url_dict):
            url_dict_template['netloc'] = ''.join((url_dict['host'],url_dict['sp_host_port'],url_dict['port']['explicit']))
        else:
            url_dict_template['netloc'] = url_dict['port']['explicit']
            if(url_dict_template['scheme'] == 'https'):
                url_dict_template['port']['implicit'] = "443"
            elif(url_dict_template['scheme'] == 'http'):
                url_dict_template['port']['implicit'] = "80"
            else:
                pass
    else:
        pass
    if('path' in url_dict):
        url_dict_template['path'] = url_dict['path']
        sec_1 = ''.join((url_dict_template['scheme'],url_dict_template['sp_scheme_host'],url_dict_template['netloc'],url_dict_template['sp_netloc_path'],url_dict['path']))
    else:
        return(''.join((url_dict_template['scheme'],url_dict_template['sp_scheme_host'],url_dict_template['netloc'])))
    if('params' in url_dict):
        url_dict_template.params = url_dict.params;
    elif('params_dict' in url_dict):
        url_dict_template['params_dict'] = url_dict['params_dict'];
        url_dict_template['params'] = params_dict_urlencode(url_dict['params_dict']);
    else:
        pass
    if(url_dict_template['params']==""):
        sec_2 = sec_1;
    else:
        sec_2 = ''.join((url_dict_template['sp_path_params'],sec_1))
    if('query' in url_dict):
        url_dict_template['query'] = url_dict['query']
        sec_3 = ''.join((sec_2,url_dict_template['sp_params_query'],url_dict_template['query']))
    elif('query_dict' in url_dict):
        url_dict_template['query_dict'] = url_dict['query_dict']
        url_dict_template['query'] = params_dict_urlencode(url_dict['query_dict'],sp="&")
        sec_3 = ''.join((sec_2,url_dict_template['sp_params_query'],url_dict_template['query']))
    else:
        return(sec_2)
    if('fragment' in url_dict):
        url_dict_template['fragment'] = url_dict['fragment']
        sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
        return(sec_4)
    elif('fragment_dict' in url_dict):
        url_dict_template['fragment_dict'] = url_dict['fragment_dict']
        url_dict_template['fragment'] = params_dict_urlencode(url_dict['fragment_dict'],sp="&")
        sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
        return(sec_4)
    else:
        if('hash' in url_dict):
            url_dict_template['hash'] = url_dict['hash']
            sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['hash']))
            return(sec_4)
        elif('hash_dict' in url_dict):
            url_dict_template['hash_dict'] = url_dict['hash_dict']
            url_dict_template['fragment'] = params_dict_urlencode(url_dict['hash_dict'],sp="&")
            sec_4 = ''.join((sec_3,url_dict_template['sp_query_fragment'],url_dict_template['fragment']))
            return(sec_4)
        else:
            return(sec_3)


def params_to_params_dict(params_str):
    eles = params_str.split(";")
    eles_len = eles.__len__()
    r1 = {}
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            kv_arr = kv.split("=")
            k=kv_arr[0]
            v=kv_arr[1]
            k=urllib.parse.unquote(k)
            v=urllib.parse.unquote(v)
            r1[k] = v
        else:
            k = kv
            v = {}
            k=urllib.parse.unquote(k)
            r1[k] = v
    return(r1)

def params_dict_urlencode(decoded_dict,sp=";"):
    eles = decoded_dict
    eles_len = eles.__len__()
    r1_dict = {}
    r2_str = ""
    for k in eles:
        if(type(eles[k]) == type({})):
            r2_str = ''.join((r2_str,sp,k))
        else:
            r1_dict[k] = eles[k]
    rslt_str = urllib.parse.urlencode(r1_dict)
    rslt_str = ''.join((rslt_str,r2_str))
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    return(rslt_str)
    

def urldecode(encoded_str,sp="&"):
    eles = encoded_str.split(sp)
    eles_len = eles.__len__()
    r1 = {}
    for i in range(0,eles_len):
        kv = eles[i]
        if("=" in kv):
            kv_arr = kv.split("=")
            k=kv_arr[0]
            v=kv_arr[1]
            k=urllib.parse.unquote(k)
            v=urllib.parse.unquote(v)
            r1[k] = v
        else:
            k = kv
            v = {}
            k=urllib.parse.unquote(k)
            r1[k] = v
    return(r1)

def urlencode(decoded_dict,sp="&"):
    eles = decoded_dict
    eles_len = eles.__len__()
    r1_dict = {}
    r2_str = ""
    for k in eles:
        if(type(eles[k]) == type({})):
            r2_str = ''.join((r2_str,sp,k))
        else:
            r1_dict[k] = eles[k]
    rslt_str = urllib.parse.urlencode(r1_dict)
    rslt_str = ''.join((rslt_str,r2_str))
    rslt_str = rslt_str.lstrip(sp)
    rslt_str = rslt_str.replace("&",sp)
    return(rslt_str)
    
