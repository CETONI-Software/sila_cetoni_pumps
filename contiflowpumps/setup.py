from setuptools import find_packages, setup

setup(
    name="contiflowpump_service",
    packages=find_packages(),
    install_requires=["sila2"],
    include_package_data=True,
)
