from setuptools import setup, find_packages

import url_health


setup(
    name='django-url-health',
    version=url_health.__version__,
    description='Check URLs',
    long_description=open('README.rst').read(),
    author='Denis Viklov',
    author_email='denis.viklov@gmail.com',
    url='https://github.com/denisviklov/django-url-health',
    license='Apache v2.0',
    packages=find_packages(exclude=['test_settings.py', 'mockapp']),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'django-jsonview>=1.2.0'
    ]
)