from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.referencedatagridfield',
      version=version,
      description="Mix of Reference and DataGrid Fields",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='archetypes referencebrowser datagrid field widget relation',
      author='Quintagroup [Andriy Mylenkyi]',
      author_email='support@quintagroup.com',
      url='http://svn.plone.org/svn/collective/collective.referencedatagridfield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.DataGridField>=1.8a1',
          'archetypes.referencebrowserwidget>=2.0a',
          # 'Products.ATReferenceBrowserWidget>=3.0a',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      # setup_requires=["PasteScript"],
      # paster_plugins=["ZopeSkel"],
      )
