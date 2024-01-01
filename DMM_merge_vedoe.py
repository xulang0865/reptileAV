import os
import subprocess

import os
import subprocess

def add_to_path(path):
    if 'PATH' in os.environ:
        os.environ['PATH'] = path + os.pathsep + os.environ['PATH']
    else:
        os.environ['PATH'] = path

def process_files(path):
    add_to_path(r'C:\Program Files\ffmpeg-6.0-full_build\bin')

    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp4')]
    max_resolution = '0x0'
    max_bitrate = 0
    min_bitrate = float('inf')

    for file in files:
        cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=height,width,bit_rate -of csv=p=0 {}'.format(file)
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split(',')
        resolution = '{}x{}'.format(output[1], output[0])
        bitrate = int(output[2])
        if resolution > max_resolution:
            max_resolution = resolution
        if bitrate > max_bitrate:
            max_bitrate = bitrate
        if bitrate < min_bitrate:
            min_bitrate = bitrate

    for file in files:
        cmd = 'ffmpeg -i {} -s {} -b:v {}k -minrate {}k -maxrate {}k temp_{}'.format(file, max_resolution, max_bitrate // 1000, min_bitrate // 1000, max_bitrate // 1000, os.path.basename(file))
        subprocess.call(cmd, shell=True)

    with open('filelist.txt', 'w') as f:
        for file in files:
            f.write("file 'temp_{}'\n".format(os.path.basename(file)))

    cmd = 'ffmpeg -f concat -safe 0 -i filelist.txt -c:v libx264 -crf 23 output.mp4'
    subprocess.call(cmd, shell=True)

    for file in files:
        os.remove('temp_{}'.format(os.path.basename(file)))
    os.remove('filelist.txt')


if __name__ == '__main__':
    add_to_path(r'C:\Program Files\ffmpeg-6.0-full_build\bin')
    process_files('tmp')