import setuptools

with open("README.MD", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRES=[
    "testops-commons"
]

setuptools.setup(
    name="testops-pytest",
    version="1.0.0",
    author="Katalon, LLC. (https://www.katalon.io)",
    author_email="info@katalon.io",
    description="Katalon TestOps PyTest Plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katalon-studio/testops-report-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords=["Katalon", "TestOps"],
    python_requires='>=3.6',
    install_requires=REQUIRES
)