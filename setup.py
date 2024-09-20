from setuptools import setup, find_packages

setup(
    name='documine',
    version='0.1.0',
    author='Areeb Syed',
    author_email='areebsyed237@gmail.com',
    description='A lightweight document mining library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sydarb/documine',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'pdfminer.six',
        'python-docx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
