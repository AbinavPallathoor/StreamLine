import subprocess
import yt_dlp
from yt_dlp import YoutubeDL
import pickle
import os.path
import time
import requests

""" File Handling """
def initialize_data(data_path = 'data.dat'):
    if os.path.isfile(data_path) == False:
        print('Creating Data File...')
        file = open('data.dat', 'wb')
        pickle.dump({}, file)
        pickle.dump({}, file)
        pickle.dump([], file)
        pickle.dump({}, file)
        file.close()
        return {}, {}, [], {}
    else:
        with open('data.dat', 'rb') as file:
            try:
                channels = pickle.load(file)
                videos = pickle.load(file)
                deleted_videos = pickle.load(file)
                listed_videos = pickle.load(file)
                return channels, videos, deleted_videos, listed_videos
            except:
                print('Error Retrieving Data')

def add_channel(channel_name):
    channel_exists = False
    try:
        with open('data.dat', 'rb') as file:
            channels_data = pickle.load(file)
            videos_data = pickle.load(file)
            deleted_data = pickle.load(file)
            listed_videos_data = pickle.load(file)
            if channel_name not in list(channels_data.keys()):
                channels_data[channel_name] = []
                print(f'Added Channel {channel_name}')
            else:
                channel_exists = True
                print('Channel Already Exists in File')
    
        if channel_exists == False:
            with open('data.dat', 'wb') as file:
                pickle.dump(channels_data, file)
                pickle.dump(videos_data, file)
                pickle.dump(deleted_data, file)
                pickle.dump(listed_videos_data, file)

        return channels_data
    except:
        print('Failed To Add Data')

def remove_channel(channel_name):
    channel_exists = True
    try:
        with open('data.dat', 'rb') as file:
            channels_data = pickle.load(file)
            videos_data = pickle.load(file)
            deleted_data = pickle.load(file)
            listed_videos_data = pickle.load(file)
            if channel_name not in list(channels_data.keys()):
                channel_exists = False
                print('Channel Doesnt Exist')
            else:
                print(f'Removing {channel_name}...')
                channels_data.pop(channel_name)
    
        if channel_exists == True:
            with open('data.dat', 'wb') as file:
                pickle.dump(channels_data, file)
                pickle.dump(videos_data, file)
                pickle.dump(deleted_data, file)
                pickle.dump(listed_videos_data, file)

        return channels_data
    except:
        print('Failed To Remove Data')


def add_video(channel, video_id, video_title, video_description):
    video_exists = False
    try:
        with open('data.dat', 'rb') as file:
            channels_data = pickle.load(file)
            videos_data = pickle.load(file)
            deleted_data = pickle.load(file)
            listed_videos_data = pickle.load(file)
            if video_id not in channels_data[channel]:
                channels_data[channel] = [video_id, video_title, video_description]
                videos_data[video_id] = [video_title, time.time(), False]
                listed_videos_data[video_id] = [channel,video_title, video_description]
            else:
                video_exists = True
                print('Video Already Exists in File')
    
        if video_exists == False:
            with open('data.dat', 'wb') as file:
                pickle.dump(channels_data, file)
                pickle.dump(videos_data, file)
                pickle.dump(deleted_data, file)
                pickle.dump(listed_videos_data, file)

        return channels_data, videos_data, listed_videos_data
    except:
        print('Failed To Add Data')

def remove_video(video_id):
    video_exists = False
    with open('data.dat', 'rb') as file:
        channels_data = pickle.load(file)
        videos_data = pickle.load(file)
        deleted_data = pickle.load(file)
        listed_videos_data = pickle.load(file)
        if video_id in list(videos_data.keys()):
            video_exists = True
            print(f"Deleting Video: {video_id}")
            videos_data.pop(video_id)
            listed_videos_data.pop(video_id)
            deleted_data.append(video_id)
            os.remove("web/"+video_id+".mp4")


    if video_exists == True:
        with open('data.dat', 'wb') as file:
            pickle.dump(channels_data, file)
            pickle.dump(videos_data, file)
            pickle.dump(deleted_data, file)
            pickle.dump(listed_videos_data, file)
    else:
        print("Video Doesnt Exist")

    return channels_data, videos_data, deleted_data, listed_videos_data

def check_video_exists(video_id, videos_data):
    if video_id in list(videos_data.keys()): return True
    else: return False

def check_video_is_deleted(video_id, deleted_videos):
    if video_id in deleted_videos: return True
    else: return False


def get_title_from_id(video_id, videos):
    for id in videos:
        if id == video_id:
            return videos[id]

def get_id_from_url(video_url):
    video_id = video_url.split('https://www.youtube.com/watch?v=')
    return video_id[1]


""" Youtube Downloading """
def download_video(video_id, duration, min_video_duration = 0, max_video_duration = 3600):
    video_url = 'https://www.youtube.com/watch?v='+video_id
    
    output_path = f'web/{video_id}.mp4'

    print('Downloading Video...')
    if duration >= min_video_duration and (max_video_duration == -1 or max_video_duration >= duration):
        # Use yt-dlp to fetch and merge video and audio
        subprocess.run([
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            '--merge-output-format', 'mp4',
            video_url,
            '-o', output_path
        ])

        print(f'Download complete: {output_path}')
    else:
        print('Video not in given time frame')

def get_recent_video_url(channel_tag):
    channel_url = f'https://www.youtube.com/{channel_tag}'
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlistend': 1,}


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract channel or playlist information
            info = ydl.extract_info(channel_url, download=False)
            entries = info['entries']
            for entry in entries[0].get('entries'):
                video_url = entry['url']
                # Getting Video Info
                with YoutubeDL(ydl_opts) as ydl:
                    # Extract video metadata
                    info = ydl.extract_info(video_url, download=False)

                    # Extract details
                    title = info.get('title', 'Unknown Title')
                    duration = info.get('duration', 0)  # Duration in seconds
                    thumbnail_url = info.get('thumbnail', None)
                    description = info.get('description', 'Description not available')

                    video_id = get_id_from_url(video_url)

                    # Download the thumbnail
                    if thumbnail_url:
                        response = requests.get(thumbnail_url, stream=True)
                        if response.status_code == 200:
                            with open("web/"+video_id+".jpg", 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)
                        else:
                            thumbnail_file_path = "Failed to download thumbnail"



                
                return video_url, title, duration, description

    except Exception as e:
        print(f'DEBUG: Error -> {e}')
        return None