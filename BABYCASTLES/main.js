var rilexicon = new RiLexicon;

var transcript;
var pictureBlob = {};

function preload() {
    mySound = loadSound('data/moon_korean.wav');
    //transcript = loadJSON('mike_sara.js', loadAPI(transcript[0].words[0][0]));
    $.getJSON('data/moon_korean.js').done(function(data) {
        transcript = data;
        associatePictures(data);
    });
}

function associatePictures(data) {
    for (var i = 0, max = data.length; i < max; i++) {
        for (var j = 0, jmax = data[i].words.length; j < jmax; j++) {
            searchWord = data[i].words[j][0];
            if (rilexicon.isNoun(searchWord) && !String.isStopWord(searchWord)) {
                if (!pictureBlob[searchWord]) {
                    pictureBlob[searchWord] = [];
                    getUrl(searchWord);
                }
            }
        }
    }
};

var startTime = 0;

function setup() {
    mySound.play();
    startTime = Date.now();
    var counterMax = transcript.length;
}

var counter = 0;

function draw() {
    // console.log(counter + " at time " + currTime(Date.now()))
    if (transcript[counter].start < currTime(Date.now())) {
        var subTranscript = transcript[counter].words;
        var line = '';
        for (var i = 0, max = subTranscript.length; i < max; i++) {
            word = subTranscript[i][0];
            line += word + ' ';
            if (pictureBlob[word]) {
                console.log(word);
                $("#imageDiv").html('<img src=' + pictureBlob[word] + ' style=\"height:500px\"/>');
            }
        }
        $("#subtitle").html(line);
    }
    if (transcript[counter].end < currTime(Date.now())) {
        counter++;
    }
}

function getUrl(searchString) {
    //console.log('request for ' + searchString);
    var photoUrl = '';
    $.getJSON("https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=572dfbfd0b23648fd7b366ab2750668f&tags=" + searchString + "&page=1&format=json&nojsoncallback=1").done(function(data) {

        var pic = {
            id: data.photos.photo[0].id,
            owner: data.photos.photo[0].owner,
            secret: data.photos.photo[0].secret,
            server: data.photos.photo[0].server,
            farm: data.photos.photo[0].farm,
            title: data.photos.photo[0].title,
        }
        photoUrl = "https://farm" + pic.farm + ".staticflickr.com/" + pic.server + "/" + pic.id + "_" + pic.secret + "_b.jpg";
        //console.log(photoUrl);
        pictureBlob[searchString].push(photoUrl);
        //console.log(searchString + ' and ' + photoUrl);
    });
}

function currTime(time) {
    return (time - startTime) / 1000;
}
