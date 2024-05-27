# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# Copyright (c) 2023, by Abhishek Chougule developer.mrabhi@gmail.com
# For license information, please see license.txt

from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in overtime_cal/__init__.py
from overtime_cal import __version__ as version

setup(
	name="overtime_cal",
	version=version,
	description="Overtime Calculation",
	author="Abhishek Chougule",
	author_email="chouguleabhis@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
