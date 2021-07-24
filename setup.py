from setuptools import setup

setup(
        name="tracemoe.py",
        author="Chrovo",
        version="0.0.1",
        description = "An simple async and sync API wrapper for the tracemoe API.",
        long_description = "This is an async and sync API wrapper for the tracemoe API, tracemoe is an anime search engine where you could trace back exactly when and where a scene happens.",
        url = "https://github.com/Chrovo/tracemoe.py",
        classifiers = ["Intended Audience::Developers", "Programming Language::Python", "Natural Language::English","Programming Languuage::Python::3"],
        install_requires = ['requests','aiohttp'],
        license = "MIT",
        packages = ["tracemoe"],
        keywords=["anime", 'tracemoe']
)
