function init() {
    var results = document.getElementById("songs");
    var query = document.getElementById("query");
    var send = document.getElementById("go");
    var spotifySearchUrl = "https://api.spotify.com/v1/search?query=$query&offset=0&limit=50&type=track"; //This is Spotify's search uri 
    var preview = document.getElementById("preview");
    var currentlyPlaying = "";
    query.focus();

    send.addEventListener("click", submitSearch);
    query.addEventListener("keyup", submitSearch);

    function submitSearch() {
        //This listener waits for the search key to be pressed and searches for the song
        preview.pause();
        results.innerHTML = "";
        var searchTerm = encodeURIComponent(query.value);
        var search = spotifySearchUrl.replace(/\$query/, searchTerm);
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var responseText = JSON.parse(xhttp.responseText);
                renderSpotifySong(responseText);
            }
        };

        xhttp.open("GET", search, true);
        xhttp.send(null);
    }

    function addToDOM(provider, cover, songName, songArtist, trackURL, previewURL) {
        //attached the song widget onto the div class songs
        var div = document.createElement("div");
        var innerDiv = '<div class="song $provider animated fadeInLeft"><img class="cover" src="$cover"><ul class="song_info"><li class="song_name">$songName</li><li class="song_artist">$songArtist</li><li class="provider"><a href="$trackURL" title="See on $provider" target="_blank"><i class="fa fa-$provider"></i></a></li></ul><div class="actions"><button type="button" class="btn preview play" id="$previewURL"><i class="fa fa-play"></i></button></div></div>';
        innerDiv = innerDiv.replace(/\$provider/g, provider);
        innerDiv = innerDiv.replace(/\$cover/, cover);
        innerDiv = innerDiv.replace(/\$songName/, songName);
        innerDiv = innerDiv.replace(/\$songArtist/, songArtist);
        innerDiv = innerDiv.replace(/\$trackURL/, trackURL);
        innerDiv = innerDiv.replace(/\$previewURL/, previewURL);

        div.innerHTML = innerDiv;

        var previewNode = div.getElementsByClassName("preview")[0];
        previewNode.addEventListener("click", audioHandler);
        results.appendChild(div);
    }

    function renderSpotifySong(response) {
        var tracks = response.tracks.items;
        for (var x = 0; x < tracks.length; x++) {
            setTimeout(function (i) {
                return function () {
                    var currentSong = tracks[i];
                    var service = "spotify";
                    var art = currentSong.album.images[1].url;
                    var song = currentSong.name;
                    var author = currentSong.artists[0].name;
                    var url = currentSong.external_urls.spotify;
                    var preview = currentSong.preview_url;
                    addToDOM(service, art, song, author, url, preview);
                };
            }(x), 0);
        }
    }

    function audioHandler() {
        if (currentlyPlaying === "") {
            currentlyPlaying = this.id;
            preview.setAttribute("src", currentlyPlaying);
            preview.play();
        } else {
            if (currentlyPlaying === this.id) {
                if (!preview.paused) {
                    preview.pause();
                } else {
                    preview.play();
                }
            } else {
                currentlyPlaying = this.id;
                preview.setAttribute("src", currentlyPlaying);
                preview.play();
            }
        }
    }


}

window.onload = init;