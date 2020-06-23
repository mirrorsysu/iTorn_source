__VERSION__ = "1.0.0"

# 是否启用代理
USE_PROXIES = True

proxies = {
    'http': '127.0.0.1:1080',
    'https': '127.0.0.1:1080'
}

# torn api key
API_KEY = "************"

# 当回复消息大于该值时，会进行切割 0则不切割
REPLY_MESSAGE_SLICE_LEN = 300