python transcribe.py;
node timestamps.js;
find . -iname '*.wav' -exec ffmpeg -loop 1 -i test.jpg -i {} -c:v libx264 -tune stillimage -c:a aac -strict experimental -b:a 192k -pix_fmt yuv420p -shortest videos/{}.mp4 \;
python clean.py;
