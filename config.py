# coding: utf-8


SECURITY_KEY = ''
TRADE_URL = 'http://222.66.233.198:8080/gateway/merchant/trade'
QUERY_URL = 'http://222.66.233.198:8080/gateway/merchant/query'
MER_ID = ''
FRONT_END_URL = ''
BACK_END_URL = ''
PREAUTH_BACK_END_URL = ''


SIGN_TYPE = 'MD5'

DEAL_TYPE = {
            'trade':'01',                    # 普通交易
            'preauth_trade':'02',            # 预授权发起 
            'preauth_complete':'03',         # 预授权完成
            'refund':'04',                   # 退货
            'preauth_refund':'04',           # 预授权退货
            'cancel':'31',                   # 交易撤销
            'preauth_cancel':'32',           # 预授权撤销
            'preauth_complete_cancel':'33',  # 预授权完成撤销
}


DEAL_STATUS = {
                'unpaid':0,
                'paid':1,
                'finished':2,
                'fail':3,
}


RESP_SUCCESS = '00'

TRANS_STATUS = {
                'success':'00',
                'processing':'01',
                'fail':'03'
                }

