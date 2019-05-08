from setuptools import setup
from setuptools import find_packages

setup(name='skypond',
      version='0.2.0',
      description='A simple reinforcement learning competition foundation',
      long_description='SkyPond is a foundation for working with and qualifying multi-agent reinforcement learning competition submissions',
      author='Rob Venables',
      author_email='rob@upkoi.com',
      url='https://github.com/upkoi/skypond',
      license='MIT',
      install_requires=['numpy>=1.9.1',
                        'docker>=3.7.2',
                        'gym>=0.12.1'],
      extras_require={
          'tests': ['pytest',
                    'pytest-pep8'],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=find_packages())
