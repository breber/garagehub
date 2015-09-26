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

* Datables: 1.10.9
* Bootstrap Datepicker: eternicode/bootstrap-datepicker@eed4bfd127bad8ff8806db345cdef1194a43f091
* jQuery Validation Engine: posabsolute/jQuery-Validation-Engine@c06327ea118cf8f900969eb27d2e337d626e0f6c
* jQuery: 2.1.4
* JS sprintf: alexei/sprintf.js@62ecd0ceeda6a865f00593d2e58bbaca1f87a12f
