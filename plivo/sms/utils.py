import json
import pkg_resources
import threading


class SingletonMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(SingletonMetaClass, cls).__init__(cls, bases, dict)
        cls._instance = None
        cls._singleton_lock = threading.Lock()

    def __call__(cls, *args):
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = super(SingletonMetaClass, cls).__call__(*args)
        return cls._instance


class CommonUtils(object):
    @staticmethod
    def deepMergeDictionaries(dict_source, dict_to_merge):
        for key in dict_to_merge:
            if key in dict_source:
                if isinstance(dict_source[key], dict) and isinstance(dict_to_merge[key], dict):
                    dict_source[key] = CommonUtils.deepMergeDictionaries(dict_source[key], dict_to_merge[key])
                else:
                    dict_source[key] = dict_to_merge[key]
            else:
                dict_source[key] = dict_to_merge[key]
        return dict_source

    @staticmethod
    def readResourceJson(module, path):
        json_string = CommonUtils.readResourceString(module, path)
        return json.loads(json_string)

    @staticmethod
    def readResourceString(module, path):
        return pkg_resources.resource_string(module, path)
