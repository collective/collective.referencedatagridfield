Introduction
============

collective.referencedatagridfield is a mix of Reference and DataGrid fields for Plone. 
This is a sophisticated reference field with its own widget for adding and deleting references 
for both internal and external resources. Having complete support for Archetype's Reference field 
functionality, it also allows external links management.

This package functionality is based on DataGridField, DataGridWidget and Archetype's Reference field
with ATReferenceBrowserWidget. It allows Plone developers to extend default Plone Reference field functionality
or override existing Reference field functionality with a custom one. 

Required Products.DataGridField package is automatically installed during installation procedure.

Development
-----------

This product was developed by Quintagroup for Plone collective, sponsored by Headnet company http://headnet.dk/.

Supported Plone Version
-----------------------

Plone 4.0

Usage
-----

There is an example of simple content type creation with a mix of Reference and DataGrid fields as related items included into the package:
http://svn.plone.org/svn/collective/collective.referencedatagridfield/collective/referencedatagridfield/examples/ReferenceDataGridDemoType.py

With this package your content types might get sophisiticated related items field: include related items from the current site and external ones.

1. *Internal Links* - to insert internal link use 'Add...' button and browse your site for the necessary object you want to add. 
Type in desirable title into the Title field. If you leave it empty - it will automatically be filled with the inserted object title.

2. *External Links* - to insert external links type in external URL into the Links field. Type in full address with  http:// protocol. 
In case your URL is not correct it will not be saved. Type in desirable title into the Title field. If you leave it empty - it will 
get title the same as URL.

Author
------

Andriy Mylenkyy 

Links
-----

* SVN Repository - http://svn.plone.org/svn/collective/collective.referencedatagridfield
* Documentation - http://projects.quintagroup.com/products/wiki/collective.referencedatagridfield


