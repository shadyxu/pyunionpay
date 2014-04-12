# coding: utf-8


# 银联分配用于MD5加密的秘钥
SECURITY_KEY = ''

# 手机支付交易地址
TRADE_URL = 'http://222.66.233.198:8080/gateway/merchant/trade'

# 手机支付查询地址
QUERY_URL = 'http://222.66.233.198:8080/gateway/merchant/query'

# 银联分配的商户ID
MER_ID = ''

# 前端/同步通知地址
FRONT_END_URL = ''

# 后端/异步通知地址
BACK_END_URL = ''

# 加密类型，目前仅支持"MD5"
SIGN_TYPE = 'MD5'

# 自定义的交易类型
DEAL_TYPE = {
            'trade':'01',                    # 普通交易
            'preauth_trade':'02',            # 预授权发起 
            'preauth_complete':'03',         # 预授权完成
            'refund':'04',                   # 退货
            'preauth_refund':'04',           # 预授权退货，同退货
            'cancel':'31',                   # 交易撤销
            'preauth_cancel':'32',           # 预授权撤销
            'preauth_complete_cancel':'33',  # 预授权完成撤销
}
