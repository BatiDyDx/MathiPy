from setuptools import setup, find_packages

setup(
    name='mathipy',
    version='0.1dev',
    packages=find_packages(),
    license='MIT',
    author='Bautista José Peirone',
    author_email='bautista.peirone@gmail.com',
    description='Math tools for python 3.x',
    url='https://github.com/BatiDyDx/MathiPy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True
)