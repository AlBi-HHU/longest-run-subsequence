import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='longestrunsubsequence',
    version='1.0.0',
    author='Sven Schrinner, Manish Goel, Michael Wulfert, Philipp Spohr, Korbinian Schneeberger, Gunnar W. Klau',
    author_email='albi@hhu.de',
    description='Algorithm to compute the longest run subsequence of a string',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AlBi-HHU/longest-run-subsequence',
    packages=setuptools.find_packages(),
    extras_require={
        'ILP-acceleration': ['PuLP>=1.6.8'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    python_requires='>=3.5',
)
