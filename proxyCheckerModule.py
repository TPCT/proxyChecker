"""
    this script is used to check if the proxy is valid or not
    :return None
"""
import requests

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


def checkProxyDict(proxyDict, website, timeOut=10):
    """
    :param timeOut: connection time out
    :param proxyDict: a valid proxy dict which containers {'http': 'ip:port', 'https': 'ip:port'}
    :param website: the website which we need to check the proxy upon it
    :return: True if proxy is valid else False
    """
    try:
        requests.request('head', website, proxies=proxyDict, timeout=timeOut)
    except Exception as e:
        return False
    return True


def isValid(proxy, website, timeout=10):
    """ :param timeout: connection timeout
        :param proxy: -> input proxy to be checked
        :param website: -> website to check the proxy on it
        :return: (validity, proxy ip, proxy port, proxy type)
    """
    proxyDict = ({'http': 'http://%s' % proxy,
                  'https': 'http://%s' % proxy},
                 {'http': 'socks4://%s' % proxy,
                  'https': 'socks4://%s' % proxy},
                 {'http': 'socks5://%s' % proxy,
                  'https': 'socks5://%s' % proxy})
    proxySplit = proxy.split(':')
    for i in range(3):
        if checkProxyDict(proxyDict[i], website, timeout):
            return True, proxySplit[0], proxySplit[1], proxyDict[i]['http'].split(':')[0]
    return False, proxySplit[0], proxySplit[1], None
