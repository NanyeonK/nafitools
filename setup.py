from setuptools import setup, find_packages

setup(
    name='nafitools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'wrds',
        'scipy',
        'statsmodels',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            # 필요한 경우 커맨드라인 스크립트 정의
        ],
    },
    author='Yeonchan Kang',
    author_email='nanyeon99@gmail.com',
    description='A description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NanyeonK/nafitools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
