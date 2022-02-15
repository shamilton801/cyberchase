from setuptools import setup

setup(
    name='cryptochase',
    version='0.0.1',
    description='Game code for TAMU Spring 2022 Turing Games',
    url='https://github.com/smh3005/cryptochase',
    author='Seth Hamilton and Trevor Bolton',
    author_email='logistics@theturinggames.com',
    license='BSD 2-clause',
    packages=['cryptochase'],
    install_requires=['perlin-noise',
                      'numpy',
                      'perlin-noise',
                      'pygame',           
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)