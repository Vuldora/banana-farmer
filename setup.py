from setuptools import setup

setup(
    name='banana_farmer',
    version='1.0',
    description='Discord bot with many useful features for BTD Battles 2',
    license='GPLv3',
    author='Vuldora',
    author_email='bnf@vuldora.com',
    packages=['banana-farmer'],
    install-requires=['requests','discord.py','python-dotenv','typing'],
)
