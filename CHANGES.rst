Changelog
=========

0.6 (unreleased)
----------------

- Fix issues populating correct link field when multiple rows are added.
  [alecpm]

- Fix title display when multiple rows reference the same UID.
  [alecpm]

- Rename ``referencedatagridwidget.js`` to ``referencedatagridwidget.min.js``
  and ``referencedatagridwidget.dev.js`` to ``referencedatagridwidget.js``.
  [thet]

- Compatibility for jQuery 1.7 + , including 1.9.Breaks compatibility with
  jQuery < 1.7, thus Plone < 4.3.
  [thet]

- Use ``linkOpaque.png`` instead of deprecated ``linkOpaque.gif``.
  [thet]

- PEP 8, JSHint.
  [thet]

- Added support for unicode title.
  [radekj]


0.5.3 (January, 11 2013)
------------------------

- fixed getting field attributes [kroman0]


0.5.2 (April, 20 2012)
----------------------

- documentation update


0.5.1 (April, 20 2012)
----------------------

- minor i18n improvements


0.5 (September, 12 2011)
------------------------

- fixed compatibility issues with Plone 4.1


0.4 (July 19, 2011)
-------------------

- Merged the more-columns branch [chervol]

- The default title for manual links is the the link [chervol]


0.3 (April 4, 2011)
-------------------

- Clashing of JS with default referencebrowserwidget fixed

- Minor fixes in templates and in javascripts


0.2 (April 1, 2011)
-------------------

- JS fixed for compatibility with archetypes.referencebrowserwidget >= 2.0rc2


0.1 (May 21, 2010)
------------------

- Initial release
