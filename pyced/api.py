import asyncio
import functools

import aiohttp
import aiohttp.web

def init(url, headers=None, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    if not headers:
        headers = {}
    http = aiohttp.ClientSession(loop=loop)
    return Api(url, http, headers)

async def post(api, path, headers, **kwargs):
    print(kwargs)
    return await api.post(path, headers=headers, data=kwargs)

async def get(api, path, headers, **kwargs):
    return await api.get(path, headers=headers, params=kwargs)

class Entity(object):
    def __init__(self, api, name, method, headers):
        self._api = api
        self._name = name
        self._method = method
        self._headers = headers

    def __getattr__(self, name):
        return functools.partial(self._method, self._name + '/' + name, self._headers)

    def __call__(self, id):
        headers = dict(self._headers)
        headers['id'] = id
        return Entity(self._api, self._name, functools.partial(post, self._api), headers)

class Api(object):
    def __init__(self, url, http, headers):
        self._url = url
        self._http = http
        self._headers = headers

    def __getattr__(self, name):
        method = functools.partial(get, self)
        return Entity(self, name, functools.partial(get, self), self._headers)

    def get_url(self, path):
        return self._url + "/" + path
    async def post(self, path, *args, **kwargs):
        return await self._http.post(self.get_url(path), *args, **kwargs)
    async def get(self, path, *args, **kwargs):
        return await self._http.get(self.get_url(path), *args, **kwargs)
