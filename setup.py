import re
import setuptools

with open('securedrop_api/__init__.py') as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='securedrop-api',
    version=version,
    author='heartsucker',
    author_email='heartsucker@autistici.org',
    description='SecureDrop API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #url=TODO
    package_dir={'securedrop_api': 'securedrop_api'},
    packages=['securedrop_api'],
    platforms='any',
    python_requires='>=3.4',
    install_requires=[
        'requests',
    ],
    classifiers=(
	'Development Status :: 2 Pre-Alpha',
	'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)
