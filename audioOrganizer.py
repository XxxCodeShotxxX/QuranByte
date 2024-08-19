import os
raw_audio = 'C:/Users/A M ! N E/Desktop/QuranByte/audio/raw/Yasser_Ad-Dussary/'

for ayah in os.listdir(raw_audio):
    surah_number = ayah[0:3]
    ayah_number = ayah[3:6]

    os.makedirs(raw_audio + surah_number,exist_ok=True)
for  ayah  in os.listdir(raw_audio):
    if ( not os.path.isdir(os.path.join(raw_audio, ayah)) ):
        surah_number = ayah[0:3]
        ayah_number = ayah[3:6]
        os.replace(raw_audio+ayah,raw_audio+surah_number+'/'+ayah_number+".mp3")

