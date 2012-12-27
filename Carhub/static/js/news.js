// Reference: https://developers.google.com/news-search/v1/devguide#hiworld

// This code generates a "Raw Searcher" to handle search queries. The Raw
// Searcher requires you to handle and draw the search results manually.
google.load('search', '1');

function searchComplete(search) {
	// Check that we got results
	$('#searchresults').empty();
	if (search.results && search.results.length > 0) {
		// iterate through search results array
		$.each(search.results, function(index, element) {
			var articleDiv = document.createElement('div');
			articleDiv.setAttribute("class", "news-articlediv news-roundedcorners linkable");

			// open article in new window when div is clicked
			articleDiv.setAttribute("onclick", "window.open('" + element.unescapedUrl + "')");

			// link to news article
			var aWrapper = document.createElement('div');
			var a = document.createElement('a');
			a.innerHTML = element.unescapedUrl;
			aWrapper.appendChild(a);

			// link title
			var linkTitle = document.createElement('h4');
			linkTitle.innerHTML = element.title;
			articleDiv.appendChild(linkTitle);

			var publishWrapper = document.createElement('div');

			// publisher information
			var publishInfo = document.createElement('span');
			publishInfo.innerHTML = "<b>" + element.publisher + "</b>";
			publishWrapper.appendChild(publishInfo);

			// published date
			publishInfo = document.createElement('span');
			var pubDate = new Date(element.publishedDate);
			publishInfo.innerHTML = pubDate.toDateString();
			publishInfo.setAttribute("class", "pull-right");
			publishWrapper.appendChild(publishInfo);

			articleDiv.appendChild(publishWrapper);
			articleDiv.appendChild(aWrapper);

			document.getElementById('searchresults').appendChild(articleDiv);
		});
	} else {
		var carMake = $('#carmake').val();
		var carModel = $('#carmodel').val();
		var carYear = $('#caryear').val();
		var noResults = document.createElement('p');
		noResults.innerHTML = "There is no recent news for the " + carYear + " " + carMake + " " + carModel + ".";
		document.getElementById('searchresults').appendChild(noResults);
	}
}

function onLoad() {
	// Create a News Search instance.
	var newsSearch = new google.search.NewsSearch();
	var carMake = $('#carmake').val();
	var carModel = $('#carmodel').val();
	var carYear = $('#caryear').val();
	// Set searchComplete as the callback function when a search is
	// complete. The newsSearch object will have results in it.
	newsSearch.setSearchCompleteCallback(this, searchComplete, [newsSearch]);
	newsSearch.setResultSetSize(8);
	// Specify search queries
	newsSearch.execute('"' + carYear + ' ' + carMake + ' ' + carModel + '"');

	// Include the required Google branding
	google.search.Search.getBranding(document.getElementById('googleBranding'));
}

// Set a callback to call your code when the page loads
google.setOnLoadCallback(onLoad);
