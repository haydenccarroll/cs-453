from setuptools import setup

package_name = 'hw2_assignment'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='haydenccarroll',
    maintainer_email='haydencarroll77@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points = {
        'console_scripts': [ 'test = hw2_assignment.main:main'],
    }
)
