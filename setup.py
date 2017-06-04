from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='boomboombot',
      version='0.1',
      description='Boom boom and boom, bot.',
      url='https://github.com/Skogarmadr/HeArcPythonBot',
      author='Luca Srdjenovic',
      author_email='luca.srdjenovic@he-arc.ch',
      license='MIT',
      packages=['boomboombot'],
      install_requires=requirements
      )
