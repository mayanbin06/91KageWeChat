#encoding=utf-8

class WxConfig(object):
    AppID = 'wx9253fa1ffd8dc814'  # AppID(应用ID)
    AppSecret = 'f86b9309c228912f4503bb0d2e778d02'  # AppSecret(应用密钥)

    '''获取access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
