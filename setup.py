from setuptools import setup, find_packages

setup(
    name='agent-oai-sdk',
    version='0.1.0',
    author='Luca Cannarozzo',
    author_email='luca.cannarozzo@unguess.io',
    description='A Python SDK for interacting with the OAI agent.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cannarocks/openai-sdk-example',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'openai-agents',
        'openai',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)