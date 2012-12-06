//Reference: https://developers.google.com/news-search/v1/devguide#hiworld 

  // This code generates a "Raw Searcher" to handle search queries. The Raw 
  // Searcher requires you to handle and draw the search results manually.
  google.load('search', '1');

  var newsSearch;
  var carMake;
  var carModel;
  var carYear;

  function searchComplete() {
    // Check that we got results
    document.getElementById('searchresults').innerHTML = '';
    if (newsSearch.results && newsSearch.results.length > 0) {
      
    	// iterate through search results array
    	for (var i = 0; i < newsSearch.results.length; i++) {
        
	        var articleDiv = document.createElement('div');
	        articleDiv.setAttribute("class", "news-articlediv news-roundedcorners");
	        
	        // open article in new window when div is clicked
	        articleDiv.setAttribute("onclick", "window.open('" + newsSearch.results[i].unescapedUrl + "')");
	        
	        // link to news article
	        var a = document.createElement('a');
	        a.href = newsSearch.results[i].unescapedUrl;
	        a.innerHTML = newsSearch.results[i].unescapedUrl;
	        a.setAttribute("class", "news-floatleft news-links");
			
	        // link title
	        var linkTitle = document.createElement('p');
	        linkTitle.setAttribute("class", "news-articletitle");
			linkTitle.innerHTML = newsSearch.results[i].title;
			articleDiv.appendChild(linkTitle);
	        
	        // publisher information
	        var publishInfo = document.createElement('span');
	        publishInfo.innerHTML = "<b>" + newsSearch.results[i].publisher + "</b>";
	        publishInfo.setAttribute("class", "news-floatleft");
	        articleDiv.appendChild(publishInfo);
	
	        // published date
	        publishInfo = document.createElement('span');
	        var pubDate = new Date(newsSearch.results[i].publishedDate);
	        publishInfo.innerHTML = pubDate.toDateString();
	        publishInfo.setAttribute("class", "news-floatright");
	        articleDiv.appendChild(publishInfo);
	        articleDiv.appendChild(a);
	
	        document.getElementById('searchresults').appendChild(articleDiv);
      	}
    }
    else {
    	var noResults = document.createElement('p');
    	noResults.innerHTML = "There is no recent news for the " + carYear + " " + carMake + " " + carModel + ".";
    	document.getElementById('searchresults').appendChild(noResults);
    }
  };

  
  function onLoad() {
    // Create a News Search instance.
    newsSearch = new google.search.NewsSearch();
    carMake = $('#carmake').val();
    carModel = $('#carmodel').val();
    carYear = $('#caryear').val();
    // Set searchComplete as the callback function when a search is 
    // complete. The newsSearch object will have results in it.
    newsSearch.setSearchCompleteCallback(this, searchComplete, null);
    newsSearch.setResultSetSize(8);
    // Specify search queries
    newsSearch.execute('"' + carYear + ' ' + carMake + ' ' + carModel + '"');
    //newsSearch.execute('"2013 Toyota Prius"');

    // Include the required Google branding
    google.search.Search.getBranding(document.getElementById('googleBranding'));
  };

  // Set a callback to call your code when the page loads
  google.setOnLoadCallback(onLoad);