import os

from enum import Enum

from plivo.sms.utils import SingletonMetaClass, CommonUtils


class Env(Enum):
    DEV = 1
    PROD = 2

    def __str__(self):
        return {
            Env.DEV: 'dev',
            Env.PROD: 'prod'
        }.get(self)

    @staticmethod
    def fromStr(env):
        return {
            'dev': Env.DEV,
            'prod': Env.PROD
        }.get(env)


class ConfigProvider(object):
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        env = Env.fromStr(os.environ.get('MOE_DEPLOYMENT_ENV') or 'dev')
        config_file = 'config.json'
        self.config = CommonUtils.readResourceJson(__name__, config_file)
        if env != Env.PROD:
            env_config = CommonUtils.readResourceJson(__name__, 'config_' + str(env) + '.json')
            self.config = CommonUtils.deepMergeDictionaries(self.config, env_config)
        self.config['env'] = env

    def getEnv(self):
        return self.config.get('env')

    def getPostGresConfig(self):
        return self.config.get('connections', {}).get('postgres', {})

    def getRedisConfig(self):
        return self.config.get('connections', {}).get('redis', {})
