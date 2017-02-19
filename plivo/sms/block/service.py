from abc import ABCMeta, abstractmethod

from plivo.sms.config.provider import ConfigProvider
from plivo.sms.utils import RedisKeyGenerator
from plivo.sms.settings import redis_store


class MessageBlocker(object):
    __metaclass__ = ABCMeta

    def __init__(self, sms_request):
        self.sms_request = sms_request

    def get_redis_key(self):
        return RedisKeyGenerator.generateBlockedMessageKey(self.sms_request.sms_from, self.sms_request.sms_to)

    @abstractmethod
    def needs_blocking(self):
        pass

    @abstractmethod
    def block_message(self):
        pass


class InboundMessageBlocker(MessageBlocker):
    def __init__(self, sms_request):
        super(InboundMessageBlocker, self).__init__(sms_request)
        self.blocked_time = ConfigProvider().getBlockTimeSecs()

    def needs_blocking(self):
        blocked_patterns = ConfigProvider().getBlockedPatterns()
        # Can use regex here for advanced pattern matching
        matched_patterns = filter(lambda pattern: self.sms_request.sms_text.strip() == pattern, blocked_patterns)
        return bool(matched_patterns)

    def block_message(self):
        redis_key = self.get_redis_key()
        return redis_store.set(redis_key, self.sms_request.sms_text, ex=self.blocked_time)


class OutboundMessageBlocker(MessageBlocker):
    def __init__(self, sms_request):
        super(OutboundMessageBlocker, self).__init__(sms_request)

    def needs_blocking(self):
        return redis_store.exists(self.get_redis_key())

    def block_message(self):
        return True