from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='forexcast',
    version='0.1.0',
    license='MIT',
    description='Simple currency forecasting for IEX data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bradley Reimers',
    author_email = 'b.a.reimers@gmail.com',
    url = 'https://github.com/IntrospectData/forexcast',
    download_url = 'https://github.com/IntrospectData/forexcast/archive/v0.1.0.tar.gz',
    keywords = ['forecast', 'finance', 'fintech', 'currency', 'fbprophet'],
    py_modules=['forexcast'],
    install_requires=[
        'Click',
        'fbprophet',
        'holidays<=0.10',
        'pandas',
        'requests',
        'plotly',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        forexcast=forexcast:main
    ''',
)
