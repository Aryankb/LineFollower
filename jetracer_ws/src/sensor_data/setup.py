from setuptools import find_packages, setup

package_name = 'sensor_data'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "infrared_data=sensor_data.infrared_data:main",
            "line_controller=sensor_data.line_controller:main",
            "ultrasonic_data=sensor_data.ultrasonic_data:main"
        ],
    },
)
