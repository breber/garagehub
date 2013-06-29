# README #
================

## Setting up Eclipse ##

* Download the [Google AppEngine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)

## Repository Layout ##

	  /
	  ├── static/
	  │   ├── css/
	  │   ├── img/
	  │   └── js/
	  ├── templates/
	  │   └── The template HTML files
	  ├── app.yaml
	  │   └── The application configuration file
	  ├── cron.yaml
	  │   └── The configuration file describing cron jobs the server runs
	  ├── index.yaml
	  │   └── The list of database indexes
	  ├── models.py (The classes defining datastore entities)
	  └── *.py (All the Python source code)

## Storing Data ##

We will be using the [NDB](https://developers.google.com/appengine/docs/python/ndb/) library for storing and retrieving data from the datastore. This library automatically caches results, which will greatly benefit us.

See `datastore.py` for examples of how to retrieve records from the database.

## API ##

We will be using [Google Cloud Endpoints](https://developers.google.com/appengine/docs/python/endpoints/) in order to set up our API for easy client library generation.

## Helpful Links ##

* [Google AppEngine](https://appengine.google.com/)
* [Python AppEngine Docs](https://developers.google.com/appengine/docs/python/)
* [Google API Console](https://code.google.com/apis/console/)
* [Twitter Bootstrap](http://getbootstrap.com)
* [jQuery](http://jquery.com/)
