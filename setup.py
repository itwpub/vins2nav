from setuptools import setup
from glob import glob

package_name = 'vins2nav'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/configs', glob('configs/*.yaml')),
        ('share/' + package_name + '/scripts', glob('scripts/*')),
        ('share/' + package_name + '/docs', glob('docs/*.md')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vins2nav',
    maintainer_email='dev@example.com',
    description='Vision navigation integration template for OAK 4Dpro + VINS-Fusion + Nav2.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
