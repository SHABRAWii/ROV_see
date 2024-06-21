from setuptools import setup

package_name = 'serial_motor_rov'

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
    maintainer='newans',
    maintainer_email='josh.newans@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gui = serial_motor_rov.gui:main',
            'driver = serial_motor_rov.driver:main',
            'newDriver = serial_motor_rov.newDriver:main'
        ],
    },
)
