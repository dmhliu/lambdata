import setuptools
from distutils.core import setup
setup(
    name='lambdata_dmhliu',         # How you named your package folder (MyLib)
    packages=['lambdata_dmhliu'],   # Chose the same as "name"
    version='0.3.2',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    description='some useful fun',   # Give a short description about your library
    long_description='A collection of data science tools',
    author='daveliu',                   # Type in your name
    author_email='dmhliu@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/dmhliu/lambdata',
    # Keywords that define your package best
    keywords=['data wrangling', 'preprocessing'],
    install_requires=[
        'pandas',
        'numpy',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
