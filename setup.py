#!/usr/bin/env python
from distutils.core import setup

setup(
        name='samklang-payment',
        version="0.4.6",
        author='Sigurd Gartmann',
        author_email='sigurdga-samklang@sigurdga.no',
        url='http://github.com/sigurdga/samklang-payment',
        description='Donations and payment app for Samklang',
        long_description=open('README.txt').read(),
        license="AGPL",
        packages = ['samklang_payment', 'samklang_payment.migrations'],
        package_data = {'samklang_payment': ['templates/samklang_payment/*.html', 'static/js/*.js', 'static/css/*.css', 'static/img/*.png', 'locale/*/LC_MESSAGES/django.*o']},
        install_requires=['pytz>=2011n','pyRFC3339>=0.1'],
        classifiers=[
                "Development Status :: 3 - Alpha",
                "License :: OSI Approved :: GNU Affero General Public License v3",
                "Intended Audience :: Developers",
                "Framework :: Django",
                "Environment :: Web Environment",
                "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                ]
        )
