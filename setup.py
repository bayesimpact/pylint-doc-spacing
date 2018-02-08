"""PyLint plugin to check the presence of a blank line after any documentation."""

import setuptools

__version__ = '0.0.3'

setuptools.setup(
    name='pylint-doc-spacing',
    packages=['pylint_doc_spacing'],
    version=__version__,
    description=__doc__,
    author='Pascal Corpet',
    author_email='pascal@bayesimpact.org',
    url='https://github.com/bayesimpact/pylint-doc-spacing',
    download_url='https://github.com/bayesimpact/pylint-doc-spacing/tarball/' + __version__,
    license='The MIT License (MIT)',
    keywords=['PyLint', 'plugin', 'convention', 'spacing'],
    install_requires=['pylint'],
    classifiers=[],
)
