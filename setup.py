from setuptools import setup
from jhsiao.namespace import make_ns, fdir
make_ns('jhsiao', dir=fdir(__file__))
setup(
    name='jhsiao-scope',
    version='0.0.1',
    author='Jason Hsiao',
    author_email='oaishnosaj@gmail.com',
    description='Get names in scope.',
    packages=['jhsiao'],
    py_modules=['jhsiao.scope']
)
