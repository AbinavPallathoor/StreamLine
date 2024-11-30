import eel
eel.init('web')

from YTFunctions import *
from concurrent.futures import ThreadPoolExecutor
import threading

channels, videos, deleted_videos, listed_videos = initialize_data(data_path = 'data.dat')


# Expose the function to get the video data
@eel.expose
def get_video_data():
    return listed_videos


# Start the Eel app
eel.start('index.html', size=(1080, 720))


""" Main Functions """
def process_channel(channel):
    global channels, videos, deleted_videos, listed_videos
    print(f'Getting Info on {channel}...')
    video_url, video_title, video_duration, video_description = get_recent_video_url('@' + channel)
    video_id = get_id_from_url(video_url)

    video_exists = check_video_exists(video_id, videos)
    video_deleted = check_video_is_deleted(video_id, deleted_videos)

    if not video_exists and not video_deleted and (len(channels[channel]) == 0 or (len(channels[channel]) == 2 and channels[channel][0] != video_id)):
        print('New Video Found!')
        channels, videos, listed_videos = add_video(channel, video_id, video_title, video_description)

        print(f'Title: {video_title},  Duration: {video_duration}, Video ID: {video_id}')
        download_video(video_id, video_duration)
    else:
        print(f'Already Exists --> {video_id}')

def download_new_videos():
    global channels  # Ensure `channels` is a global variable as it seems to be
    with ThreadPoolExecutor() as executor:
        # Submit a separate thread for each channel
        executor.map(process_channel, channels)

def delete_expired_videos(expiry_time = 172800):
    global channels, videos, deleted_videos
    for video_id in videos:
        if videos[video_id][1] < time.time() + expiry_time:
            channels, videos, deleted_videos, listed_videos = remove_video(video_id)


# Call the main function
def run_periodically(func, interval):
    def wrapper():
        func()
        while True:
            time.sleep(interval)
            func()
            delete_expired_videos()

    thread = threading.Thread(target=wrapper, daemon=True)  # Run as a daemon thread
    thread.start()

run_periodically(download_new_videos, 300)