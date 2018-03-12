#encoding=utf-8

class WxConfig(object):
    AppID = 'wx21512b184ce97f79'  # AppID(应用ID)
    AppSecret = '3dc1427af974bfe5b34b39408574038b'  # AppSecret(应用密钥)

    '''获取access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
