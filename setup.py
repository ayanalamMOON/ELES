from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eles",
    version="0.1.0",
    author="E.L.E.S. Team",
    author_email="contact@eles-project.org",
    description="Extinction-Level Event Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        'streamlit>=1.28.0',
        'pyyaml>=6.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'matplotlib>=3.7.0',
        'scikit-learn>=1.3.0',
        'plotly>=5.15.0',
        'seaborn>=0.12.0',
        'requests>=2.31.0'
    ],
    entry_points={
        'console_scripts': [
            'eles-cli=run_cli:main',
            'eles-web=run_app:main'
        ],
    },
)
