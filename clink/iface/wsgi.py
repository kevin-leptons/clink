from abc import ABC, abstractmethod


class IWsgi(ABC):
    @abstractmethod
    def __call__(self, wsgi_env, wsgi_send):
        '''
        WSGI inteface

        :param dict wsgi_env:
        :param function wsgi_send:
        '''

        pass
