window.onload = function(){
$.getJSON('https://pypi.org/pypi/sunpy/json', function(data) {
	document.getElementById('version').innerHTML = data.info.version;
});
};
