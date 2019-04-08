import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='unicorn_binance_websocket_api',
     version='1.0.0',
     scripts=['unicorn_binance_websocket_api'],
     author="UNICORN Data Analysis, www.unicorn-data.com",
     author_email="it@ml.unicorn-data.com",
     description="A python API to use the Binance Websocket API in a easy, fast, robust and fully-featured way.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/unicorn-data-analysis/unicorn-binance-websocket-api",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3.6.1",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)