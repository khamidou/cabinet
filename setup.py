from distutils.core import setup
setup(name='cabinet',
      version='0.1',
      description='A thin layer over BerkeleyDB',
      author='Karim Hamidou',
      author_email='khamidou@etu.utc.fr',
      py_modules=['cabinet'],
      data_files=[('.', ['README'])] 
      )
