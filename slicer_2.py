print("Slicer 2!")
source_file = input("Nazwa pliku źródłowego: ")

def artist():
    global multiple_artists
    
    artists_prompt = input("Podaj ilość wykonawców.\n1: Jeden wykonawca\n2: Wielu wykonawców\n")

    if(artists_prompt == "1"):
        multiple_artists = False
        print("Wybrano jednego wykonawcę.\n")
        global track_artist
        track_artist = input("Wykonawca albumu: ")
        
    elif(artists_prompt == "2"):
        multiple_artists = True
        print("Wybrano wielu wykonawców.")
        
    else:
        print("Podaj poprawną wartość.")
        artist()


def end_or_duration():
    global end_type
    end_or_duration_prompt = input("\nZnasz przedziały trwania czy czasy trwania poszczególnych utworów?\n1: Przedziały trwania\n2: Czasy trwania\n")

    if(end_or_duration_prompt == "1"):
        end_type = True
        print("Wybrano przedziały trwania.\n")

    elif(end_or_duration_prompt == "2"):
        end_type = False
        print("Wybrano czas trwania poszczególnych utworów.\n")
        
    else:
        print("Podaj poprawną wartość.\n")
        end_or_duration()


def array_track_info():
    global track_artist
    global album_title
    global album_info
    total_time = 0
    album_info = {}

    track_artist_prompt = "Wykonawca {} utworu: "
    track_title_prompt = "Tytuł {} utworu: "
    track_endtime_prompt = "Koniec {} utworu: "
    track_duration_prompt = "Długość {} utworu: "

    album_title = input("Podaj tytuł albumu: ")
    tracks = int(input("Podaj ilość utworów na albumie: "))

    for i in range(1, tracks+1):
        track_number = i
        if(multiple_artists==True):
            track_artist = input(track_artist_prompt.format(i))
        
        track_title = input(track_title_prompt.format(i))
        
        if(end_type==True):
            print("test")
            track_endtime_raw = input(track_endtime_prompt.format(i))
            track_endtime = sum(x * int(t) for x, t in zip([60, 1], track_endtime_raw.split(":")))
            track_duration = track_endtime - total_time
            track_startime = track_endtime - track_duration
            total_time = track_endtime
        
        if(end_type==False):
            track_duration_raw = input(track_duration_prompt.format(i))
            track_duration = sum(x * int(t) for x, t in zip([60, 1], track_duration_raw.split(":")))
            track_endtime = total_time + track_duration
            track_startime = track_endtime - track_duration
            total_time = track_endtime
       
        track_array = [track_artist, track_title, album_title, track_number, track_duration, track_startime, track_endtime]
        album_info.update({i: track_array})
    print(album_info)


def slice_audio():
    from pydub import AudioSegment
    import os
    global album_info
    global output_folder
    global source_file
    
    song = AudioSegment.from_mp3(source_file)
    album_name = str(album_info.get(1)[2])


    current_dir = os.getcwd()
    
    output_folder = current_dir + "/" + album_name
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for i in range(1, len(album_info)+1):
        start = album_info.get(i)[5]*1000
        end = album_info.get(i)[6]*1000
        file_name = str(album_info.get(i)[3]) + ". " + str(album_info.get(i)[0]) + " - " + str(album_info.get(i)[1])

        song_slice = song[start:end]
        song_slice.export(output_folder + "/" + file_name + ".mp3", format="mp3")
        
        print(start)
        print(end)


def album_info_to_csv():
    import csv
    from csv import writer
    global album_info
    
    track_array = ["track_artist", "track_title", "album_title", "track_number", "track_duration", "track_startime", "track_endtime"]

    album = album_info
    output_file = output_folder + "/" + str(album_info.get(1)[2]) + ".csv"

    with open(output_file, 'w') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(track_array)

    for x in album.values():
        with open(output_file, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(x)
            f_object.close() 

artist()
end_or_duration()
array_track_info()
slice_audio()
album_info_to_csv()
