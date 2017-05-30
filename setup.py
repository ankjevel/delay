from setuptools import setup, find_packages

setup(
    name="delay",
    version="0.0.1",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Flask', 'flask_limiter', 'Flask-Common',
    ],
)
