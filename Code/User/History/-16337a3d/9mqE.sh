# ffmpeg -i STREAM_URL -f segment -segment_time 30 -strftime 1 %s.mp4 -v verbose 2>&1 |  grep -Po --line-buffered "Opening '\\K\\d+" |  xargs -I _ bash -c 'echo; date -d @_; inotifywait -qqe CLOSE _.mp4; whisper --model medium.en _.mp4'
# ffmpeg -nostdin -threads 0 -i $INPUT_AUDIO_FILE -f wav -ac 1 -acodec pcm_s16le -ar 16000 - | whisper.cpp -m models/ggml-tiny.en.bin -f -
