from setuptools import setup, find_packages

# Function to parse the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as f:
        # Filter out empty lines and comments
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='Supreme-Court-Judgment-Docs-Chunker',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    description='This setup.py will install all dependencies for you',
    author='Vihaan Nama',
    author_email='vihaan.nama@outlook.com',
)