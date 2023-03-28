from setuptools import setup, find_packages
import pathlib

current = pathlib.Path(__file__).parent.resolve()

long_description = (current / "README.md").read_text(encoding="utf-8")

setup(
    name='dns',
    version='1.0.0',
    description='A Network Attack Tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Hassan-Al-Achek/netdeath.git',
    author="Hassan Al ACHEK - 0xh41",
    author_email="0xh41@protonmail.com",
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Topic :: Security',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Networking, TCP/IP, UDP, DNS, DHCP, Spoofing, MITM',
    project_urls={
        'Documentation': 'https://github.com/Hassan-Al-Achek/netdeath/blob/main/README.md',
        'Funding': '',
        'Source': 'https://github.com/Hassan-Al-Achek/netdeath.git',
        'Tracker': 'https://github.com/Hassan-Al-Achek/netdeath/issues',
    },
    packages=find_packages(),
    install_requires=['scapy', 'inquirer', 'terminaltables'],
    python_requires='>=3',
)

# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#distributing-packages
