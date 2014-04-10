# coding: utf-8
# author: xujun

import urllib
import urlparse
from hashlib import md5
from datetime import datetime
import random
import re

import config 


def build_request(type, *args, **kwargs):
    if type == 'trade':
        para = build_trade_para(*args, **kwargs)
    elif type == 'refund':
        para = build_refund_para(*args, **kwargs)
    elif type == 'cancel':
        para = build_cancel_para(*args, **kwargs)
    elif type == 'query':
        para = build_query_para(*args, **kwargs)
    elif type == 'preauth_trade':
        para = build_preauth_trade_para(*args, **kwargs)
    elif type == 'preauth_complete':
        para = build_preauth_complete_para(*args, **kwargs)
    elif type == 'preauth_cancel':
        para = build_preauth_cancel_para(*args, **kwargs)
    elif type == 'preauth_complete_cancel':
        para = build_preauth_complete_cancel_para(*args, **kwargs)
    para = filter_para(para)
    para['signature'] = sign(para)
    para['signMethod'] = config.SIGN_TYPE
    return create_link_string(para, False, True)


def _build_trade_para(order_num, amount, desc, type):
    """构造交易类请求参数"""
    para = {'version':'1.0.0',
            'charset':'UTF-8',
            'transType':config.DEAL_TYPE[type],
            'merId':config.MER_ID,
            'backEndUrl':config.BACK_END_URL,
            'frontEndUrl':config.FRONT_END_URL,
            'orderDescription':desc.encode('utf-8') if desc else desc,
            'orderTime':datetime.now().strftime('%Y%m%d%H%M%S'),
            'orderNumber':order_num,
            'orderAmount':amount,
            'orderCurrency':'156',
            'reqReserved':'reqReserved',
            }
    return para


def build_trade_para(order_num, amount, desc):
    return _build_trade_para(order_num, amount, desc, 'trade') 


def build_preauth_trade_para(order_num, amount, desc):
    return _build_trade_para(order_num, amount, desc, 'preauth_trade') 


def _build_post_trade_para(order_num, amount, qn, type):
    """构造后交易请求参数, post_trade, 类似post season"""

    para = {'version':'1.0.0',
            'charset':'UTF-8',
            'transType':config.DEAL_TYPE[type],
            'merId':config.MER_ID,
            'backEndUrl':config.BACK_END_URL,
            'orderTime':datetime.now().strftime('%Y%m%d%H%M%S'),
            'orderNumber':order_num,
            'orderAmount':amount,
            'orderCurrency':'156',
            'qn':qn,
            'reqReserved':'reqReserved',
            }
    return para


def build_cancel_para(order_num, amount, qn):
    return _build_post_trade_para(order_num, amount, qn, 'cancel')


def build_preauth_complete_para(order_num, amount, qn):
    return _build_post_trade_para(order_num, amount, qn, 'preauth_complete')


def build_preauth_cancel_para(order_num, amount, qn):
    return _build_post_trade_para(order_num, amount, qn, 'preauth_cancel')


def build_preauth_complete_cancel_para(order_num, amount, qn):
    return _build_post_trade_para(order_num, amount, qn, 'preauth_complete_cancel')


def build_refund_para(order_num, amount, qn):
    return _build_post_trade_para(order_num, amount, qn, 'refund')


def build_query_para(order_num, type, deal_time):
    para = {'version':'1.0.0',
            'charset':'UTF-8',
            'transType':config.DEAL_TYPE[type],
            'merId':config.MER_ID,
            'orderTime':deal_time,
            'orderNumber':order_num,
            #'merReserved':'reserved'
            }
    return para


def create_link_string(para, sort, encode):
    """对参数排序并拼接成query string的形式"""
    if sort:
        para = sorted(para.items(), key=lambda d:d[0])
    if encode:
        return urllib.urlencode(para)
    else:
        ps = ''
        for p in para:
            if ps:
                ps = '%s&%s=%s' % (ps, p[0], p[1]) 
            else:
                ps = '%s=%s' % (p[0], p[1]) 
        return ps 


def filter_para(para):
    """过滤空值和签名"""
    for k,v in para.items():
        if not v or k in ['signature', 'signMethod']:
            para.pop(k) 
    return para
        

def sign(para):
    """签名, 目前只支持md5签名
    @param para dict
    @return 签名 str"""
    para_str = create_link_string(para, True, False)
    para_str = '%s&%s' % (para_str, md5(config.SECURITY_KEY).hexdigest())
    return md5(para_str).hexdigest()


def parse_resp(qs):
    """解析query string"""
    qs = urllib.unquote(qs)
    rst = {}
    braces = re.findall('.+(&.+=\{.+\}).+', qs)
    for brace in braces:
        index = brace.find('=')
        rst[brace[1:index]] = brace[index+1:]
        index = qs.find(brace)
        qs = qs[:index] + qs[index+len(brace):]
    rst.update(dict(urlparse.parse_qsl(qs)))
    return rst 
        

def verify_response(resp):
    """验证回复"""
    resp = parse_resp(resp)
    sig_is_valid = verify_signature(resp)
    return sig_is_valid, resp 


def verify_signature(para):
    """验证签名"""
    resp_sig = para.get('signature')
    para = filter_para(para)
    sig = sign(para) 
    return resp_sig and sig == resp_sig 


def generate_deal_num(order_num):
    return int('%s%s%s01' % (datetime.now().strftime('%y%m%d%H%M%S'), int(str(order_num)[-3:]), random.randint(10, 99)))

