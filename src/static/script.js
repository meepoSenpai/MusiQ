function button_vote(obj, song_id, weight) {
    song = jQuery(obj).closest("form").find("input:hidden").val();
    // console.log(song);
    // song = song.replace(/'/g, '"');
    // console.log(song);
    // song_id = JSON.parse(song);
    console.log("Called vote with " + song_id + " and " + weight);
    if (weight != 1 && weight != -1) {
        console.log("Weight does not seem to be right ...");
        return false;
    }

    $.ajax({
        type: "POST",
        url: "/vote",
        data: { song_id: song_id, weight: weight },
        success: function(response) {
            console.log("Got a response from the server: " + response)
            if (response == "True") {
                if (weight == 1) { obj.style.backgroundColor = "LightGreen"; };
                if (weight == -1) { obj.style.backgroundColor = "OrangeRed"; };
                var karma_element = document.getElementById('karma_' + song_id);

                $.get( "/getKarma", {song: song} , function( data ) {
                    karma_element.innerHTML = data
                });
            }
        }
    });
    return false;
};