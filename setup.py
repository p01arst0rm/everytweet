from setuptools import setup

setup(
    name='Everytweet',
    version='1.0.0',
    description='Twitter dictionary prefix bot for python 3.7',
    url='https://ever3st.com/Programs/Scripts/Everytweet/',
    author='p01arst0rm',
    author_email='polar@ever3st.com',
    license='MIT',
    packages=['Everytweet'],
    install_requires=['tweepy>=3.6.0'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    zip_safe=False)
