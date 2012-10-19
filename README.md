# README #
================

## Setting up Eclipse ##

*	Install the [PyDev Plugin for Eclipse](http://pydev.org/download.html)
	*	It would probably be best to install everything from the update URL
*	Download the [Google AppEngine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
*	Install some web development tools (that offer syntax highlighting and code completion for
JavaScript, CSS, HTML, etc...
	*	Under the Juno software site, navigate to `Web, XML, Java EE and OSGi Enterprise Development`
		*	Eclipse Java Web Developer Tools
		*	Eclipse Web Developer Tools
		*	Eclipse XML Editors and Tools
		*	JavaScript Development Tools

## Google App Engine ##

[Google App Engine](http://appengine.google.com/) is a service that allows you to build
web applications on Google's infrastructure.

When you have been added to the AppEngine application, it should show up in the list of
"My Applications" on appengine.google.com. When you navigate to the application, you can see
a lot of information. There is information about how much of the daily quota we have used so
far for the current day. You can view all the entities in the Datastore. You can see logs
from the Java code.

## Eclipse Project ##

In Eclipse, you'll want to be in the PyDev perspective.

	  CarHub/
	  ├── static/
	  │   ├── css/
	  │   ├── img/
	  │   └── js/
	  ├── templates/
	  │   └── The template HTML files - similar to the JSP pages
	  ├── app.yaml
	  │   └── The application configuration file
	  ├── index.yaml
	  │   └── The list of database indexes
	  ├── models.py (The classes defining datastore entities)
	  └── *.py (All the python source code)

## Storing Data ##

We will be using the [NDB](https://developers.google.com/appengine/docs/python/ndb/) library for storing and retrieving data from the datastore. This library automatically caches results, which will greatly benefit us.


## Helpful Links ##

*	[Google AppEngine](https://appengine.google.com/)
*	[Google API Console](https://code.google.com/apis/console/)
*	[Twitter Bootstrap](http://twitter.github.com/bootstrap)
*	[jQuery](http://jquery.com/)
