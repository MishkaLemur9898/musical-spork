import pygame
from tkinter import *
from tkinter import ttk
from os import listdir
from mutagen.mp3 import MP3

playing = False
play_btn = None
pause_btn = None
is_started = False
playing_index = 0
current_song_time = 0
should_be_playing = False
expanded = False
songs = None
last_selected = None

song_name = ""
current_playlist = None
new_playlists_folders = []
path_to_songs = None
ALBUM = []

def onselect(evt):
    #Shows the selected note on the screen
    global last_selected
    try:
        w = evt.widget
        last_selected = int(w.curselection()[0])
    except:
        last_selected = None
    

def pause_or_play():
    global playing
    global should_be_playing
    global play_btn
    global pause_btn
    global is_started
    global current_song_time
    global song_name
    global path_to_songs
    global ALBUM

    if len(ALBUM) == 0 or path_to_songs == None:
        return None
    
    if not playing:
        play_btn.place_forget()
        pause_btn.place(x = 250, y = 400)
        playing = True
        if not is_started:
            song = MP3(path_to_songs + "\\" + ALBUM[playing_index])
            current_song_time = int(song.info.length * 1000)
            pygame.mixer.music.play()
            is_started = True
        else:
            pygame.mixer.music.unpause()
        song_name = ALBUM[playing_index]
    else:
        pause_btn.place_forget()
        play_btn.place(x = 250, y = 400)
        playing = False
        pygame.mixer.music.pause()

def next_song():
    global playing
    global is_started
    global playing_index
    global current_song_time
    global song_name
    global path_to_songs

    if path_to_songs == None:
        return None
    
    if playing_index < len(ALBUM) - 1:
        playing_index += 1
        song = MP3(path_to_songs + "\\" + ALBUM[playing_index])
        current_song_time = int(song.info.length * 1000)
        pygame.mixer.music.load(path_to_songs + "\\" + ALBUM[playing_index])
        song_name = ALBUM[playing_index]
        if playing:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.play()
            pygame.mixer.music.pause()

def choose_btn():
    global songs
    global last_selected
    global current_playlist
    if not last_selected == None:
        ALBUM = listdir("PlayLists\\" + new_playlists_folders[last_selected])
        songs.delete(0, END)
        current_playlist = last_selected
        for i in ALBUM:
            songs.insert(END, i.replace(".mp3",""))

def expand_now():
    global expanded
    if expanded:
        expanded = False
        app.geometry("600x600")
    else:
        expanded = True
        app.geometry("1000x600")

def prev_song():
    global playing
    global is_started
    global playing_index
    global current_song_time
    global song_name
    global path_to_songs

    if path_to_songs == None:
        return None
    
    if playing_index > 0 :
        playing_index -= 1
        song = MP3(path_to_songs + "\\" + ALBUM[playing_index])
        current_song_time = int(song.info.length * 1000)
        pygame.mixer.music.load(path_to_songs + "\\" + ALBUM[playing_index])
        song_name = ALBUM[playing_index]
        if playing:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.play()
            pygame.mixer.music.pause()
            
def play_playlist():
    global playing_index
    global path_to_songs
    global current_playlist
    global playing_index
    global ALBUM
    global song_name
    global song
    global playing
    global current_song_time
    
    if len(listdir("PlayLists\\" + new_playlists_folders[current_playlist])) == 0:
        return None
    playing_index = 0
    path_to_songs = "PlayLists\\" + new_playlists_folders[current_playlist]
    ALBUM = []
    for i in listdir(path_to_songs):
        ALBUM.append(i)
    playing_index = 0
    try:
        song = MP3(path_to_songs + "\\" + ALBUM[playing_index])
        current_song_time = int(song.info.length * 1000)
        pygame.mixer.music.load(path_to_songs + "\\" + ALBUM[playing_index])
        song_name = ALBUM[playing_index]
    except:
        return None
    if playing:
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
    
def main():
    global app
    global play_btn
    global pause_btn
    global song_name
    global song_var
    global songs
    
    pygame.init()
    app = Tk()
    app.geometry("600x600")
    app.configure(bg= "yellow")
    app.title("Music App")
    app.iconbitmap("Music.ico")
    
    #Play Button:
    play = PhotoImage(file="Button.png")
    small_play = play.subsample(5,5)
    play_btn = Button(image=small_play,width=100,height= 100, bg = "yellow", command = pause_or_play)
    play_btn.place(x = 250, y = 400)

    #Pause Button:
    pause = PhotoImage(file="Pause.png")
    small_pause = pause.subsample(3,3)
    pause_btn = Button(image=small_pause,width=100,height= 100,bg = "yellow")
    pause_btn.config(command = pause_or_play)

    #Next Button:
    nextt = PhotoImage(file="Next.png")
    small_next = nextt.subsample(2,2)
    next_btn = Button(image=small_next,width=100,height= 100,bg = "yellow")
    next_btn.config(command = next_song)
    next_btn.place(x = 400, y = 400)

    #Prev Button:
    prev = PhotoImage(file="Prev.png")
    small_prev = prev.subsample(2,2)
    prev_btn = Button(image=small_prev,width=100,height= 100,bg = "yellow")
    prev_btn.config(command = prev_song)
    prev_btn.place(x = 100, y = 400)

    #progress bar:
    progress_bar = ttk.Progressbar(app, orient =HORIZONTAL, length = 400, mode='determinate')
    progress_bar.place(x = 100, y = 350)

    #Music Image:
    img = PhotoImage(file = "Music.png")
    img = img.subsample(2,2)
    music_logo = Label(image = img, width = 260, height = 210, bg = "yellow")
    music_logo.place(x = 180, y = 80)

    #Song Name:
    song_var = StringVar(value=song_name)
    song_name_label = Label(textvariable = song_var , bg = "yellow", font = (None, 14))
    song_name_label.place(x = 100, y = 320)
    

    #Expand:
    expand = PhotoImage(file="Expand.png")
    small_expand = expand.subsample(2,2)
    expand_button = Button(image = small_expand, width = 50, height = 50, bg = "yellow")
    expand_button.config(command = expand_now)
    expand_button.place(x = 550, y= 0)

    
    #Listbox of PlayLists:
    PlayLists = Listbox(height = 5, bg = "#8DC286", width = 35, font = (None, 13))
    PlayLists.place(x = 640, y = 50)
    PlayLists.bind('<<ListboxSelect>>', onselect)

    #PlayLists:
    PlayLists_folders = listdir("PlayLists")
    global new_playlists_folders
    for folder in PlayLists_folders:
        if not "." in folder:
            new_playlists_folders.append(folder)
            PlayLists.insert(END, folder)
    

    #Listbox of songs:
    songs = Listbox(height = 7, bg = "#8DC286", width = 35, font = (None, 13))
    songs.place(x = 640, y = 270)

    #Choose Button:
    choose = Button(width = 20, height = 3, text = "Choose PlayList", font = (None, 12))
    choose.config(command = choose_btn)
    choose.place(x = 700, y = 170)

    #Choose song:
    choose_song = Button(width = 20, height = 3, text = "Play", font = (None, 12))
    choose_song.config(command = play_playlist)
    choose_song.place(x = 700, y = 440)

    volume = [0.5]

    def plus_volume():
        if volume[0] >= 0.9:
            return
        volume[0] += 0.1
        volume_bar['value'] = round(volume[0],2) * 100
        pygame.mixer.music.set_volume(round(volume[0],2))

    def minus_volume():
        if volume[0] <= 0.1:
            return
        volume[0] -= 0.1
        volume_bar['value'] = round(volume[0],2) * 100
        pygame.mixer.music.set_volume(round(volume[0],2))
    
    #Plus button:
    plus = PhotoImage(file="Plus.png")
    plus = plus.subsample(4,4)
    plus_btn = Button(width = 40, height = 40, image=plus, bg = "yellow")
    plus_btn.config(command = plus_volume)
    plus_btn.place(x = 370, y = 550)

    #Minus button:
    minus = PhotoImage(file="Minus.png")
    minus = minus.subsample(4,4)
    minus_btn = Button(width = 40, height = 40, image=minus, bg = "yellow")
    minus_btn.config(command = minus_volume)
    minus_btn.place(x = 190, y = 550)

    #Volume Level:
    vlm_label = Label(text = "Volume", font= (None, 15), bg = "yellow")
    vlm_label.place(x = 270, y = 525)

    #volume bar:
    volume_bar = ttk.Progressbar(app, orient =HORIZONTAL, length = 100, mode='determinate')
    volume_bar.place(x = 255, y = 560)
    
    pygame.mixer.init()
    #pygame.mixer.music.load(path_to_songs + "\\" + ALBUM[0])
    
    #Volume when starting the app:
    pygame.mixer.music.set_volume(0.5)
    volume_bar['value'] = 0.5 * 100

    
    def update_bar():
        if not current_song_time == 0:
            song_var.set(song_name.replace(".mp3",""))
            percentage = pygame.mixer.music.get_pos()/current_song_time * 100
            progress_bar['value'] = percentage
            if bool(pygame.mixer.music.get_busy()) == False:
                next_song()
        app.after(300, update_bar)

    
    app.after(300, update_bar)
    app.mainloop()

if __name__ == "__main__":
    main()
