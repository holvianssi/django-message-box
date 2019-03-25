from setuptools import find_packages
from setuptools import setup

setup(
    name='holvi-messagebox',
    version='1.0.0',
    author='Holvi Payment Services Ltd',
    author_email='team@holvi.com',
    packages=find_packages(),
    install_requires=[
        'django>=1.8',
    ],
    extras_require={
        'inbox': ['djangorestframework>=2.4.10'],
        'outbox': ['celery-once>=0.1.2', 'celery>=4.1'],
    }
)
