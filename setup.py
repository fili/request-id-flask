#-*- coding:utf-8 -*-

from setuptools import (
    find_packages,
    setup
)


with open('README.md', 'r', encoding='utf-8') as f:
    read_me = f.read()

setup(
    name='request-id-flask',
    version='0.0.4',
    description='Receive and return the value of HTTP X-Request-ID header.',
    long_description=read_me,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/fili/request-id-flask',
    author='Fili',
    author_email='dev@fili.com',
    test_suite='tests',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'flask',
        'uuid',
        'quart'
    ],
)
