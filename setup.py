from setuptools import setup, find_packages

setup(name='pydec',
    version='0.0.1',
    description='DDD, ES CQRS stack',
    author='Jin-Xu',
    author_email='jnxy@lostwire.net',
    license='BSD',
    zip_safe=False,
    include_package_data=True,
    install_requires = [
        'asyncio',
        'aiohttp',
        'aio-pika',
        'aiohttp-session',
        'configparser2',
    ],
    packages=find_packages())
