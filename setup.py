from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="Cartograpy",
    version="0.1",
    author="Jiahang Li",
    author_email = "1178328479@qq.com",
    description="models for summer internship",
    long_description=readme,
    packages=find_packages(),
    url = "https://github.com/Djokovic0311/cartography.git",
    platforms = "any",
    install_requires=[]
)