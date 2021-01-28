import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='longest-run-subsequence-pkg-guwekl',
    version='1.0.0',
    author='Sven Schrinner, Manish Goel, Michael Wulfert, Philipp Spohr, Korbinian Schneeberger, Gunnar W. Klau',
    author_email='gunnar.klau@hhu.de',
    description='Algorithm to determine to longest run subsequence.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AlBi-HHU/longest-run-subsequence',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)