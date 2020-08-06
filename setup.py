import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

with open('requirements.txt') as req:
    requirements = list(filter(None, [x if 'github.com' not in x else None for x in req.read().split('\n')]))

EXCLUDE_FROM_PACKAGE = ['docs', 'tests*']

setuptools.setup(
    name="downloader",
    version="0.0.1",
    license="N/A",
    author="Pieter van der Westhuizen",
    author_email="pieter@spatialedge.co.za",
    description="Schedule downloads",
    long_description_content_type="text/markdown",
    url="for-later",
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGE),
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        downloader=downloader.cli:main
    ''',
    setup_requires=['wheel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
