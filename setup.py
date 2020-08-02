import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="ih",
    version="0.0.5",
    author="Katie McLaughlin",
    author_email="katie@glasnt.com",
    description="A very persuasive package, for creating embroidery patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glasnt/ih",
    install_requires=["click", "pillow", "tabulate"],
    entry_points={"console_scripts": ["ih = ih.cli:main"]},
    packages=["ih"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
)
