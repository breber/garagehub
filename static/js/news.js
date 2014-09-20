// Reference: https://datamarket.azure.com/dataset/bing/search#schema

function searchComplete(search) {
	// Check that we got results
	$('#searchresults').empty();
	if (search.d.results && search.d.results.length > 0) {
		// iterate through search results array
		$.each(search.d.results, function(index, element) {
			var articleDiv = document.createElement('div');
			articleDiv.setAttribute("class", "news-articlediv news-roundedcorners linkable");

			// open article in new window when div is clicked
			articleDiv.setAttribute("onclick", "window.open('" + element.Url + "')");

			// link to news article
			var aWrapper = document.createElement('div');
			var a = document.createElement('a');
			a.innerHTML = element.Url;
			aWrapper.appendChild(a);

			// link title
			var linkTitle = document.createElement('h4');
			linkTitle.innerHTML = element.Title;
			articleDiv.appendChild(linkTitle);

			var publishWrapper = document.createElement('div');

			// publisher information
			var publishInfo = document.createElement('span');
			publishInfo.innerHTML = "<b>" + element.Source + "</b>";
			publishWrapper.appendChild(publishInfo);

			// published date
			publishInfo = document.createElement('span');
			var pubDate = new Date(element.Date);
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

$(document).ready(function() {
	var vehicleId = getVehicleId();

	$.get('/news/' + vehicleId, function(data) {
		searchComplete(data);
	});
});
