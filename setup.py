from setuptools import setup

setup(
        name='distribute',
        packages=['distribute'],
        include_package_data=True,
        install_requires=[
            'flask',
        ],
        setup_requires=[
            'pytest-runner',
        ]
)
