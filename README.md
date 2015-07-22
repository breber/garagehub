# README

## Repository Layout

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

## Storing Data

We will be using the [NDB](https://developers.google.com/appengine/docs/python/ndb/) library for storing and retrieving data from the datastore. This library automatically caches results, which will greatly benefit us.

See `datastore.py` for examples of how to retrieve records from the database.

## API

We will be using [Google Cloud Endpoints](https://developers.google.com/appengine/docs/python/endpoints/) in order to set up our API for easy client library generation.

## Bootstrap

We use a custom build of Bootstrap. The only differences are some custom colors.

Copy the `static/css/garagehub.less` from our repository into the `less` folder of the Bootstrap repo. Add `@import "garagehub.less";` to the `bootstrap.less` file right after the `@import "variables.less";` line. Then build bootstrap, and copy the updated JS and CSS to the corresponding location in the repo.

## Helpful Links

* [Google AppEngine](https://appengine.google.com/)
* [Python AppEngine Docs](https://developers.google.com/appengine/docs/python/)
* [Google API Console](https://code.google.com/apis/console/)
* [Bootstrap](http://getbootstrap.com)
* [jQuery](http://jquery.com/)

## External Libraries

* Datables: 1.9.4
* Datables Bootstrap: DataTables/Plugins@cbe8320d3a09c727c50500a0f35e7783ca2c02c5
* Bootstrap Datepicker: eternicode/bootstrap-datepicker@eed4bfd127bad8ff8806db345cdef1194a43f091
* jQuery Validation Engine: posabsolute/jQuery-Validation-Engine@95f72042c61e4d8b8f1f3fe1a8451f2dbc9ebf9c
* jQuery: 2.0.3
* JS sprintf: alexei/sprintf.js@0260e01c7162ee3e9c76ca9bd24c4a1377c185e8
* TableTools: 1.9.4
