from distutils.core import setup

setup(
    name='money-bot',
    description='Telegram bot for accounting money',
    author='Ravil Latypov',
    author_email='ravillatypov12@gmail.com',
    url='https://github.com/Ravillatypov/money-account-bot',
    version='0.1.0',
    py_modules=['money_bot'],
    python_requires='~=3.7',
    install_requires=['aiogram~=2.8', 'aiohttp~=3.6.2', 'tortoise-orm~=0.16.12'],
)
