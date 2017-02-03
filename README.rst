|License MIT| | |Build Status| | |Coveralls Status| | |Codecov Status| | |Code Climate|

================
Python Daily Med
================

This library interacts with the United States National Library of Medicine's Daily
Med API.

Installation
============

* Install Python requirements ``pip install -r ./requirements``

Setup
=====

* 

Usage
=====

* `Read The API Documentation <https://laslabs.github.io/python-daily-med>`_

Import and Instantiate
----------------------

Importing an instantiating the Daily Med object:

.. code-block:: python

   from daily_med import DailyMed
   dm = DailyMed()

Structured Product Label Metadata
---------------------------------

`get_spls` mirrors the `/spls` interface as documented `here
<https://dailymed.nlm.nih.gov/dailymed/webservices-help/v2/spls_api.cfm`_.

To get an iterator of all SPLs:

.. code-block:: python

   spl_metas = dm.get_spls()

You can also perform an SPL search using any of the standard query parameters:

.. code-block:: python

   simvastatin_metas = dm.get_spls(drug_name='Simvastatin')

Structured Product Label Documents
----------------------------------

Once you have a `set_id` for an SPL, you can get its document:

.. code-block:: python

   spl_document = dm.get_spl('0be2e371-1f05-48d7-8f2e-f2024f3305f3')

An SPL Document is basically just a dictionary representing the parsed XML
document.

Known Issues / Road Map
=======================

-  SPLDocument is only Python 2 compatible. Generate a Python3 version and integrate
   an import switch for py2/3. Downfall is that this will add another 6mb of code to
   the repo & coverage will be inaccurate because not everything is testable at once.

Credits
=======

Images
------

* LasLabs: `Icon <https://repo.laslabs.com/projects/TEM/repos/odoo-module_template/browse/module_name/static/description/icon.svg?raw>`_.

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Maintainer
----------

.. image:: https://laslabs.com/logo.png
   :alt: LasLabs Inc.
   :target: https://laslabs.com

This module is maintained by LasLabs Inc.

.. |Build Status| image:: https://api.travis-ci.org/LasLabs/python-daily-med.svg?branch=master
   :target: https://travis-ci.org/LasLabs/python-daily-med
.. |Coveralls Status| image:: https://coveralls.io/repos/LasLabs/python-daily-med/badge.svg?branch=master
   :target: https://coveralls.io/r/LasLabs/python-daily-med?branch=master
.. |Codecov Status| image:: https://codecov.io/gh/LasLabs/python-daily-med/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/LasLabs/python-daily-med
.. |Code Climate| image:: https://codeclimate.com/github/LasLabs/python-daily-med/badges/gpa.svg
   :target: https://codeclimate.com/github/LasLabs/python-daily-med
.. |License MIT| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: AGPL-3
