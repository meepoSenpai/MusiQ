function button_vote(obj, song_id, weight) {
	console.log("Called vote with " + song_id + " and " + weight);
	obj.style.backgroundColor = "green";
	$.post( "/vote", { song_id: song_id, weight: weight } );
	return false;
};