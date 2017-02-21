from plivo.sms.config.provider import ConfigProvider
from plivo.sms.app import redis_store
from plivo.sms.utils import RedisKeyGenerator


class RateLimitService(object):
    def __init__(self, sms_from):
        self.sms_from = sms_from

    def get_redis_key(self):
        return RedisKeyGenerator.generateRateLimitKey(self.sms_from)

    def needs_blocking(self):
        redis_key = self.get_redis_key()
        current_count = redis_store.get(redis_key)
        if current_count is None:
            redis_store.set(redis_key, 1, ex=ConfigProvider().getRateLimitResetSecs(), nx=True, xx=False)
            current_count = 1
        if int(current_count) >= ConfigProvider().getRequestCountThreshold():
            return True
        else:
            redis_store.incr(redis_key, 1)
        return False
