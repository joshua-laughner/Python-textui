from distutils.core import setup
import sys

if sys.version_info.major == 2:
    extra_dependencies = ['backports']
else:
    extra_dependencies = []

versionstr = '0.1'
setup(
    name='pytui',
    packages=['pytui'], # this must be the same as the name above for PyPI
    version=versionstr,
    description='A text-based UI system',
    author='Josh Laughner (firsttempora)',
    author_email='first.tempora@gmail.com',
    #url='https://github.com/firsttempora/JLLUtils', # use the URL to the github repo
    #download_url='https://github.com/firsttempora/JLLUtils/tarball/{0}'.format(versionstr), # version must be a git tag
    keywords=['UI', 'user interface', 'text-based'],
    classifiers=[],
    install_requires=extra_dependencies,
)