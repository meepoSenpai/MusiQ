function button_vote(obj, song_id, weight) {
	console.log("Called vote with " + song_id + " and " + weight);
	if (weight != 1 && weight != -1) {
		console.log("Weight does not seem to be right ...");
		return false;
	}

	obj.style.backgroundColor = obj.style.color;

    var karma_element = document.getElementById('karma_' + song_id);
    var karma = karma_element.innerHTML;
    karma = Number(karma) + weight;
    karma_element.innerHTML = karma;

	$.post( "/vote", { song_id: song_id, weight: weight } );
	return false;
};