import os

if __name__ == "__main__":
    with open('config.txt') as f:
        lines = f.read().splitlines()
    filtered_lines = list(filter(lambda line: line and line[0] != '#', lines))
    dict = {}
    for line in filtered_lines:
        line = line.strip()
        pair = line.split("=")
        dict[pair[0]] = pair[1]

    print('Starting video transform....')

    first_2pass_cmd = 'ffmpeg -i ' + dict['input_file'] + \
                      ' -b:v ' + dict['video_bit_rate'] + ' -c:v ' + dict['video_codec'] + \
                      ' -pix_fmt ' + dict['pix_fmt'] + ' -crf ' + dict['crf'] + \
                      ' -c:a ' + dict['audio_codec'] + ' -b:a ' + dict['audio_bit_rate'] + \
                      ' -ar ' + dict['audio_sample_rate'] + ' -ac ' + dict['audio_channels'] + \
                      ' -pass 1 -f mp4 NUL'
    print('Starting first pass command:')
    print(first_2pass_cmd)
    os.system(first_2pass_cmd)
    print('First pass completed!')

    second_2pass_cmd = 'ffmpeg -i ' + dict['input_file'] + \
                       ' -b:v ' + dict['video_bit_rate'] + ' -c:v ' + dict['video_codec'] + \
                       ' -pix_fmt ' + dict['pix_fmt'] + ' -crf ' + dict['crf'] + \
                       ' -c:a ' + dict['audio_codec'] + ' -b:a ' + dict['audio_bit_rate'] + \
                       ' -ar ' + dict['audio_sample_rate'] + ' -ac ' + dict['audio_channels'] + \
                       ' -pass 2 -f mp4 ' + dict['output_file']
    print('Starting second pass command:')
    print(second_2pass_cmd)
    os.system(second_2pass_cmd)
    print('Second pass completed!')
    if dict['60fps'] != 'no':
        print("Starting change to 60fps, this may take a long time depends on your computer's hardware and video's size")
        os.system('ffmpeg -i ' + dict['output_file'] + ' -filter:v "minterpolate=fps=60" -c:a copy output.60fps.mp4')
        print('The output file is: output.60fps.mp4')
    else:
        print('The output file is: ' + dict['output_file'])

