import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
import re

# Configurações do Spotify
SPOTIPY_CLIENT_ID = "SUA ID CLIENT"
SPOTIPY_CLIENT_SECRET = "SUA CHAVE SECRETA"
SPOTIPY_REDIRECT_URI = "http://localhost:5000"
SCOPE = "playlist-read-private"

# Autenticação automática no Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# 🔹 Função para extrair o ID da playlist a partir do link
def extract_playlist_id(playlist_url):
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    return match.group(1) if match else None

# 🔹 Pede ao usuário um link da playlist do Spotify
playlist_url = input("Cole o link da playlist do Spotify: ")
playlist_id = extract_playlist_id(playlist_url)

if not playlist_id:
    print("❌ Link de playlist inválido!")
    exit()

# Obtendo as faixas da playlist
results = sp.playlist_tracks(playlist_id)
tracks = results["items"]

# 🔹 Função para baixar músicas usando yt-dlp
def download_song(song_name, artist_name):
    search_query = f"{song_name} {artist_name} audio"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{artist_name} - {song_name}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{search_query}"])
        print(f"✅ Download concluído: {song_name} - {artist_name}")

    except yt_dlp.utils.DownloadError as e:
        if "Sign in to confirm your age" in str(e) or "This video may be inappropriate" in str(e):
            print(f"❌ Pulando (necessário login): {song_name} - {artist_name}")
        else:
            print(f"❌ Erro ao baixar {song_name} - {artist_name}: {e}")

# 🔹 Iterar sobre as músicas e baixar
for track in tracks:
    song = track["track"]["name"]
    artist = track["track"]["artists"][0]["name"]
    print(f"🎵 Baixando: {song} - {artist}")
    download_song(song, artist)

print("✅ Todos os downloads possíveis foram concluídos!")
