from setuptools import setup

package_name = 'my_turtle_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Esha',
    maintainer_email='you@example.com',
    description='Turtle movement package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'move_turtle = my_turtle_package.move_turtle:main',  # <--- important
            'goto = my_turtle_package.goto:main',
        ],
    },
)
