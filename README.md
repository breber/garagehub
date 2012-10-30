# README #
================

## Setting up Eclipse ##

*	Install the [PyDev Plugin for Eclipse](http://pydev.org/download.html)
	*	It would probably be best to install everything from the update URL
*	Download the [Google AppEngine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
*	Install some web development tools (that offer syntax highlighting and code completion for
JavaScript, CSS, HTML, etc...
	*	Under the Juno software site, navigate to `Web, XML, Java EE and OSGi Enterprise Development`
		*	Eclipse Web Developer Tools
		*	Eclipse XML Editors and Tools
		*	JavaScript Development Tools

## Google App Engine ##

[Google App Engine](http://appengine.google.com/) is a service that allows you to build
web applications on Google's infrastructure.

When you have been added to the AppEngine application, it should show up in the list of
"My Applications" on appengine.google.com. When you navigate to the application, you can see a lot of information. There is information about how much of the daily quota we have used so far for the current day. You can view all the entities in the Datastore. You can see logs from the Java code.

## Repository Layout ##

In Eclipse, you'll want to be in the PyDev perspective.

	  /
	  ├── AutoInfo/
	  │   └── The original site prototype in Java/JSP
	  ├── CarHub/
	  │   ├── static/
	  │   │   ├── css/
	  │   │   ├── img/
	  │   │   └── js/
	  │   ├── templates/
	  │   │   └── The template HTML files - similar to the JSP pages
	  │   ├── app.yaml
	  │   │   └── The application configuration file
	  │   ├── cron.yaml
	  │   │   └── The configuration file describing cron jobs the server runs
	  │   ├── index.yaml
	  │   │   └── The list of database indexes
	  │   ├── models.py (The classes defining datastore entities)
	  │   └── *.py (All the python source code)
	  └── Documents/
	      └── The design documents/presentations

## Storing Data ##

We will be using the [NDB](https://developers.google.com/appengine/docs/python/ndb/) library for storing and retrieving data from the datastore. This library automatically caches results, which will greatly benefit us.

See `datastore.py` for examples of how to retrieve records from the database.

## Styling HTML ##

All of our custom styling will be in the file `Carhub/static/css/auto.css`. This CSS file is included on all HTML pages, and will define custom classes for use in our application.

To keep this file organized, we will have the global classes at the top of the file. Then classes and rules specific to a certain page will be prefixed with the name of that page. This way we do not accidentally override previous CSS rules that worked on a different page.

	/* global classes */
	.center { ... }
	
	/* news.html */
	.news-title { ... }
	.news-float { ... }
	
	...

## Helpful Links ##

*	[Google AppEngine](https://appengine.google.com/)
*	[Google API Console](https://code.google.com/apis/console/)
*	[Twitter Bootstrap](http://twitter.github.com/bootstrap)
*	[jQuery](http://jquery.com/)
