var fs = require('fs');

// pass name of the file as a string
function timestamps(filename) {
    var timestamp_array = [];
    var text = JSON.parse(fs.readFileSync(filename, 'utf8'));
    var lineCount = 1;
    var srtString = '';

    for (var t in text) {
        var srt = {};
        var tempTime = [];
        tempTime = text[t].start.toString().split('.');
        if (!tempTime[1]) {
            tempTime[1] = '';
        };
        if (tempTime[1].length < 4) {
            for (var i = 0, max = tempTime[1].length; i < (3 - max); i++) {
                tempTime[1] += '0';
            }
        }
        if (tempTime[0].length < 2) {
            tempTime[0] = '0' + tempTime[0];
        }

        srt.start = tempTime[0] + ',' + tempTime[1];
        tempTime = text[t].end.toString().split('.');
        if (!tempTime[1]) {
            tempTime[1] = '';
        };
        if (tempTime[1].length < 4) {
            for (var i = 0, max = tempTime[1].length; i < (3 - max); i++) {
                tempTime[1] += '0';
            }
        }
        if (tempTime[0].length < 2) {
            tempTime[0] = '0' + tempTime[0];
        }

        srt.end = tempTime[0] + ',' + tempTime[1];
        srt.words = ""
        for (var w in text[t].words) {
            // console.log(text[t].words[w][0]);
            srt.words += text[t].words[w][0] + " ";
        }
        timestamp_array.push(srt);
        srtString += lineCount + '\n' + '00:00:' + srt.start + ' --> ' + '00:00:' + srt.end + '\n' + srt.words + '\n' + '\n';
        lineCount++;
    }

    //return srtString;
    fs.writeFile(filename.split('.')[0] + '.srt', srtString, function(err) {
        if (err) {
            return console.log(err);
        }
        console.log("File saved");
    });
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

fs.readdir('./', function(err,files){
    for (var f in files){
        if (endsWith(files[f], ".js")){
            if (endsWith(files[f], "timestamps.js")){
                // do nothing
            } else {
                timestamps(files[f]);    
            }
        }
    }
});
