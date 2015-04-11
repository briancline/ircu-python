from setuptools import setup

from ircu.consts import version_str


setup(
    name='ircu',
    version=version_str,
    author='Brian Cline',
    author_email='brian.cline@gmail.com',
    description=('An IRC network state machine for Undernet ircu-based '
                 'services using the P10 protocol.'),
    long_description=open('README.rst').read(),
    license='MIT',
    keywords='irc ircu service p10',
    url='https://github.com/briancline/ircu-python',
    packages=['ircu'],
    install_requires=open('requirements.txt').readlines(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: AIX',
        'Operating System :: POSIX :: HP-UX',
        'Operating System :: POSIX :: IRIX',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: POSIX :: BSD :: BSD/OS',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: NetBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
