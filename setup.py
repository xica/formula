from distutils.core import setup

setup(
    name='formula',
    version='0.2.0',
    py_modules=['formula'],
    author='XICA',
    author_email='info@xica.net',
    url='https://github.com/xica/formula',
    description='Safe arithmetic expression evaluator',
    long_description="""Formula is a simple arithmetic expression evaluator written in Python.
The main goal of this library is to provide a safer way to evaluate
basic math expressions given in string form.
Internally, it implements a (simplified) version of Dijkstra's "shunting-
yard algorithm".""",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
