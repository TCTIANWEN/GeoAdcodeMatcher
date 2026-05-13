from setuptools import setup, find_packages

setup(
    name='geoadcode-matcher',
    version='1.0.0',
    description='行政区划代码匹配工具 - 通过省、市、县名称匹配行政代码',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='GeoAdcodeMatcher Team',
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
    ],
    extras_require={
        'tk': ['tkinter'],
    },
    entry_points={
        'console_scripts': [
            'geo-match=geoadcode_matcher.cli:main',
        ],
        'gui_scripts': [
            'geo-match-gui=geoadcode_matcher.gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)