from setuptools import setup


setup(
    name='visaxrated',
    version='0.2.1',
    description='Get exchange rates for Visa.',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    license='BSD',
    url='https://github.com/aino/visaxrated',
    packages=['visaxrated'],
    install_requires=['beautifulsoup4>=4.4.0', 'requests>=2.7.0'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
