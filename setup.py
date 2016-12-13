"""Setup mailroom madness module."""


from setuptools import setup

setup(
    name="echo server",
    description="Build an echo server using Python sockets",
    version=0.1,
    author=["Claire Gatenby", "Rachel Wisecarver"],
    author_email="clairejgatenby@gmail.com",
    licencse="MIT",
    package_dir={'': 'src'},
    py_modules=["linked_list"],
    extras_require={
        "test": ["pytest", "pytest-cov", "tox"]
    }
)
