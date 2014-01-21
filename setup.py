from setuptools import setup, find_packages

setup(
    name='pawn',
    version='0.1.0',
    url='http://github.com/j2labs/pawn',
    description='Servers for Humans.',
    license='BSD',
    author='James Dennis',
    author_email='jdennis@gmail.com',
    packages=[
        'pawn',
        'pawn.connections',
        'pawn.handlers',
        'pawn.messages',
        'pawn.servers'
    ],
    include_package_data=True,
    install_requires=[
        'gevent',
    ],
    entry_points={'console_scripts': [
        'pawn = pawn.commands:run_it',
    ]},
    classifiers=[
        'Framework :: Pawn',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Server Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
