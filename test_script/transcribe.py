import re, sys, subprocess, os, json

def convert_to_wav(files):
    '''Converts files to a format that pocketsphinx can deal wtih (16khz mono 16bit wav)'''
    converted = []
    for f in files:
        new_name = f + '.temp.wav'
        subprocess.call(['ffmpeg', '-i', f, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', new_name])
        converted.append(new_name)
    return converted

def transcribe(files=[], pre=10, post=50):
    '''Uses pocketsphinx to transcribe audio files'''

    total = len(files)

    for i, f in enumerate(files):
        #print str(i+1) + '/' + str(total) + ' Transcribing ' + f
        filename = f.replace('.temp.wav', '') + '.transcription.txt'
        transcript = subprocess.check_output(['pocketsphinx_continuous', '-infile', f, '-time', 'yes', '-logfn', '/dev/null', '-vad_prespeech', str(pre), '-vad_postspeech', str(post)])

        with open(filename, 'w') as outfile:
            outfile.write(transcript)

        os.remove(f)


def convert_timestamps(f):
    '''Converts pocketsphinx transcriptions to usable timestamps'''

    sentences = []

    # for f in files:

    #     if not f.endswith('.transcription.txt'):
    #         f = f + '.transcription.txt'
    with open(f, 'r') as infile:
        lines = infile.readlines()

    lines = [re.sub(r'\(.*?\)', '', l).strip().split(' ') for l in lines]
    lines = [l for l in lines if len(l) == 4]

    seg_start = -1
    seg_end = -1

    for index, line in enumerate(lines):
        word, start, end, conf = line
        if word == '<s>' or word == '<sil>' or word == '</s>':
            if seg_start == -1:
                seg_start = index
                seg_end = -1
            else:
                seg_end = index

            if seg_start > -1 and seg_end > -1:
                words = lines[seg_start+1:seg_end]
                start = float(lines[seg_start][1])
                end = float(lines[seg_end][1])
                if words:
                    sentences.append({'start': start, 'end': end, 'words': words, 'file': f})
                if word == '</s>':
                    seg_start = -1
                else:
                    seg_start = seg_end
                seg_end = -1

    return sentences

raw_recordings = []

for f in os.listdir(os.getcwd()):
    if f.endswith(".wav"):
        raw_recordings.append(str(f))
        continue
    else:
        continue

converted = convert_to_wav(raw_recordings)
transcribe(files=converted)

for f in os.listdir(os.getcwd()):
    if f.endswith(".transcription.txt"):
        data = convert_timestamps(f)
        # print data
        filename = f.split('.')[0]
        with open(filename + '.js', 'w') as outfile:
            json.dump(data, outfile)

for f in os.listdir(os.getcwd()):
    if f.endswith(".js"):
        # script = 'timestamps.js ' + str(f)
        print str(f)
        subprocess.call(['node', 'timestamps.js', str(f)])

# transcribe(convert_to_wav(['mike_sarah.wav']))

# print json.dumps(convert_timestamps(['moon_korean.wav.transcription.txt']))

