from setuptools import setup, find_packages

setup(
    name='PriceTracker',
    packages=['pricetracker'],
    package_dir={'pricetracker': 'src/pricetracker'},
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
