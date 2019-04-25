import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

# TODO - fix so this works
# with open("requirements.txt", "r") as f:
#    requirements = f.read()

setuptools.setup(
    name="ih",
    version="0.0.0-dev20",
    author="Katie McLaughlin",
    author_email="katie@glasnt.com",
    description="A very persuasive package, for creating embroidery patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/glasnt/ih",
    install_requires=["click", "pillow"],
    entry_points={"console_scripts": ["ih = ih.__main__:main"]},
    packages=["ih"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
)
