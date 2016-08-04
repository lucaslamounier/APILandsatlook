# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

version = '0.1'

setup(name='APILandsatlook',
      version=version,
      description="ApiLandsatlook api to get data from usgs landsatlook",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Lucas Lamounier',
      author_email='lucasls.oas@gmail.com',
      url='https://github.com/lucaslamounier',
      license='Copyright © Lucas Lamounier',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['requests'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
