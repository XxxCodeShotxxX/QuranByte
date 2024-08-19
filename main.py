import requests
from keys import api_key, ayat_count
import random
import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip,ColorClip,AudioFileClip,concatenate_audioclips
def get_background_video():
    page_number = random.randint(1, 15)
    video_number = random.randint(1, 12)
    url = f"https://api.pexels.com/videos/search?query=galaxy%20landscape&orientation=portrait&page={page_number}&size=large"
    headers={"Authorization": api_key}
    response = requests.get(url,headers=headers)


    for video in response.json()["videos"][video_number]["video_files"]:
        if(len(video["link"].split("1080_1920")) == 2):
            file_name = video["link"].split("/")[-1]
            download_response = requests.get(video["link"],stream=True)
            print("start downloading...")
            with open('videos/' + file_name, 'wb') as f :
                for chunk in download_response.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk) 

            print ("%s downloaded!\n"%file_name )



def validate_surah_number(surah_num):

    if 1 <= int(surah_num) <= 9:
        return f"00{surah_num}"
    elif 10 <= int(surah_num) <= 99:
        return f"0{surah_num}"
    elif 100 <= int(surah_num) <= 286:
        return surah_num
    else:
        return None

def validate_ayah_number(surah_num,ayah_num):
    
    if ayat_count[surah_num-1] >= ayah_num:
        return ayah_num
    else:
        return None

def video_make(video_path, surah_num, first_ayah_num, last_ayah_num):

    video_clip = VideoFileClip(video_path).without_audio()
    
    audio_clips = []
    ayat_start = 0
    for i in range(first_ayah_num, last_ayah_num + 1):
        ayah_num = validate_ayah_number(surah_num, i)
        recitation = AudioFileClip(f"audio/raw/Yasser_Ad-Dussary/{validate_surah_number(surah_num)}/{validate_surah_number(ayah_num)}.mp3")
        audio_clips.append(recitation)
        ayat_start += recitation.duration

    final_audio = concatenate_audioclips(audio_clips)
    total_duration = final_audio.duration

    repeated_video_clip =  vfx.loop(video_clip, duration=total_duration)

    overlay = ColorClip(size=repeated_video_clip.size, color=(0, 0, 0)).set_opacity(0.5).set_duration(total_duration)

    ayat_clips = []
    ayat_start = 0

    for i in range(first_ayah_num, last_ayah_num + 1):
        ayah_num = validate_ayah_number(surah_num, i)
        recitation = AudioFileClip(f"audio/raw/Yasser_Ad-Dussary/{validate_surah_number(surah_num)}/{validate_surah_number(ayah_num)}.mp3")
        
        ayah_image_clip = ImageClip(f"images/ayah png/{surah_num}_{ayah_num}.png").set_start(ayat_start).set_duration(recitation.duration)
        
        video_w, video_h = repeated_video_clip.size
        ayah_w, ayah_h = ayah_image_clip.size
        ayah_position = ('center', (video_h - ayah_h) / 2)
        ayah_image_clip = ayah_image_clip.set_position(ayah_position)

        ayat_clips.append(ayah_image_clip)
        ayat_start += recitation.duration

    surah_num = validate_surah_number(surah_num)
    surah_image_clip = ImageClip(f"images/calligrapher/png/{surah_num}.png").set_duration(total_duration).set_position('top')

    final_clip = CompositeVideoClip([repeated_video_clip, overlay, surah_image_clip] + ayat_clips).set_audio(final_audio)
    final_clip.write_videofile('looped.mp4', fps=60, codec="libx264")
video_make("videos/4250244-uhd_1440_2160_30fps.mp4",5,4,4)



