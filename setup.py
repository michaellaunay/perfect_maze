from setuptools import setup, find_packages

setup(
        name='maze',
        version='0.1.4',
        description="A perfect maze generator.",
        url='https://github.com/michaellaunay/perfect_maze',
        author='Michaël Launay',
        author_email='michaellaunay@ecreall.com',
        licence="AGPL",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        zip_safe=False
)


