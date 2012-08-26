# README #
================

## Setting up Eclipse ##

*	Install the [Google Plugin for Eclipse](https://developers.google.com/eclipse/docs/download)
	*	It would probably be best to install everything from the update URL
*	Install some web development tools (that offer syntax highlighting and code completion for
JavaScript, JSP, CSS, HTML, etc...
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

The Eclipse project is similar to all other Java projects. It has a `src` folder that contains
all of the Java code for the project. In addition, it has a `war` folder that contains all
of the static content that can be accessed on the website (such as JS, HTML, CSS, images,
JSP, etc).

Inside the `war` directory, there should be a `WEB-INF` directory. This directory contains
the files specific to Google App Engine. The `lib` directory is where all the .jar files
should go.  The `appengine-web.xml` file contains some information about the application
and how it will run on AppEngine. The `cron.xml` file contains cron jobs that are run at
a certain interval (such as retrieving an updated list of cars, or emailing a weekly report).
The `web.xml` file contains information about servlet mappings. This essentially maps a
URL path to a Java class that `HttpServlet`.

For example:

	<servlet>
		<servlet-name>DeleteAllVehicles</servlet-name>
		<servlet-class>edu.se319.team1.autoinfo.servlets.DeleteAllVehicles</servlet-class>
	</servlet>
	<servlet-mapping>
		<servlet-name>DeleteAllVehicles</servlet-name>
		<url-pattern>/admin/deletevehicles</url-pattern>
	</servlet-mapping>

Maps the path `http://website.com/admin/deletevehicles` to the Java class `edu.se319.team1.autoinfo.servlets.DeleteAllVehicles`.

	package edu.se319.team1.autoinfo.servlets;
	
	public class DeleteAllVehicles extends HttpServlet {
		public void doGet(HttpServletRequest req, HttpServletResponse resp) {
			// Do stuff...
		}
	}
