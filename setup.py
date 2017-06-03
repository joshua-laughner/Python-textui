from distutils.core import setup
versionstr = '0.1'
setup(
    name='pytui',
    packages=['pytui'], # this must be the same as the name above for PyPI
    version=versionstr,
    description='A text-based UI system',
    author='firsttempora',
    author_email='first.tempora@gmail.com',
    #url='https://github.com/firsttempora/JLLUtils', # use the URL to the github repo
    #download_url='https://github.com/firsttempora/JLLUtils/tarball/{0}'.format(versionstr), # version must be a git tag
    keywords=['UI', 'user interface', 'text-based'],
    classifiers=[],
)