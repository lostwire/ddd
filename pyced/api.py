import asyncio
import functools

import aiohttp
import requests
import aiohttp.web

def init(url, headers=None):
    if not loop:
        loop = asyncio.get_event_loop()
    if not headers:
        headers = {}
    http = aiohttp.ClientSession()
    return Api(url, http, headers, loop)

def init_sync(url, headers=None):
    if not headers:
        headers = {}
    return Synchron(url, requests.Session(), headers)

class Entity(object):
    def __init__(self, api, name, method, headers):
        self._api = api
        self._name = name
        self._method = method
        self._headers = headers

    def __getattr__(self, name):
        return functools.partial(self._method, self._name + '/' + name, self._headers)

    def __call__(self, id=None):
        headers = dict(self._headers)
        if id:
            headers['id'] = id
        return Entity(self._api, self._name, self._api.post, headers)

class Api(object):
    def __init__(self, url, http, headers, loop):
        self._url = url
        self._http = http
        self._headers = headers
        self._loop = loop

    def __getattr__(self, name):
        return Entity(self, name, self.get, self._headers)

    def get_url(self, path):
        return self._url + "/" + path
    def get_results(self, callback):
        output = self._loop.run_until_complete(callback)
        return output
    def post(self, path, headers, **params):
        self.get_results(self._http.post(self.get_url(path), data=params, headers=headers))
    def get(self, path, headers, **params):
        return self.get_results(self._http.get(self.get_url(path), params=params, headers=headers))

class Synchron(object):
    def __init__(self, url, http, headers):
        self._url = url
        self._http = http
        self._headers = headers
    def get_url(self, path):
        return self._url + "/" + path
    def __getattr__(self, name):
        return Entity(self, name, self.get, self._headers)
    def get_results(self, results):
        return results.json()
        return [{'name':'costam'}]
        return results
    def post(self, path, headers, **params):
        self._http.post(self.get_url(path), data=params, headers=headers)
        return ''
    def get(self, path, headers, **params):
        return self.get_results(self._http.get(self.get_url(path), params=params, headers=headers))

