var fs = require('fs');

// pass name of the file as a string
function timestamps(filename){
	var timestamp_array = [];
	var text = JSON.parse(fs.readFileSync(filename, 'utf8'));

	for (var t in text){
		var srt = {};
		srt.start = text[t].start
		srt.end = text[t].end
		srt.words = ""
		for (var w in text[t].words){
			// console.log(text[t].words[w][0]);
			srt.words += text[t].words[w][0] + " ";
		}
		timestamp_array.push(srt);
	}	

	return timestamp_array;
}