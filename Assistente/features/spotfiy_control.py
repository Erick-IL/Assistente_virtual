from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from Assistente.core.recognition import recognizer
from Assistente.core.tts import TTS
import spotipy
import os

# recomendar uma playlist com base nas ultimas musicas

class SpotifyController:
    def __init__(self):
        load_dotenv()
        self.tts = TTS()
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = "http://localhost:8888/callback"
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id, 
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-read-playback-state user-modify-playback-state playlist-read-private user-library-modify"
        ))
        

    def search_info(self, info: dict, method: str, index: int = 0) -> dict:
        """choose search method. 
        single: search in current playback
        multiple: search in search results
        """

        if method == 'single':
            return self._extract_single_music_info(info)
        elif method == 'multiple':
            return self._extract_multiple_music_info(info, index)

    def _extract_single_music_info(self, info: dict) -> dict:
        """Extract music information from json response. (single)"""

        artists = [artist['name'] for artist in info['item']['album']['artists']]
        return {
            "artist": artists,
            "album_name": info['item']['album']["name"],
            "music_name": info['item']["name"],
            "release_date": info['item']['album']["release_date"],
            "id": info['item']['album']['id'],
            "uri": info['item']['uri'],
            'link': info['item']['album']['external_urls']['spotify']
        }

    def _extract_multiple_music_info(self, info: dict, index: int) -> dict:
        """Extract music information from json response. (multiple)"""

        artists = [artist['name'] for artist in info['tracks']['items'][index]['artists']]
        return {
            "artist": artists,
            "album_name": info['tracks']['items'][index]['album']["name"],
            "music_name": info['tracks']['items'][index]["name"],
            "release_date": info['tracks']['items'][index]['album']["release_date"],
            "id": info['tracks']['items'][index]['album']['id'],
            "uri": info['tracks']['items'][index]['uri'],
            'link': info['tracks']['items'][index]['album']['external_urls']['spotify']
        }

    def control_playback(self, text: str):
        """Control playback of Spotify music. (play, pause, next, previous)""" 

        if 'pausar' in text or 'parar' in text or 'pause' in text:
            self._pause_playback()
        elif 'continuar' in text or 'play' in text or 'retomar' in text:
            self._start_playback()
        elif 'passar' in text or 'proxima' in text or 'pular' in text:
            self._next_track()
        elif 'voltar' in text or 'retornar' in text:
            self._previous_track()

    def _pause_playback(self):
        try:
            self.sp.pause_playback()
            self.tts.play_tts_audio("Reprodução pausada")
        except Exception as e:
            self._handle_playback_error(e)

    def _start_playback(self):
        try:
            self.sp.start_playback()
            self.tts.play_tts_audio("Reprodução retomada")
        except Exception as e:
            self._handle_playback_error(e)

    def _next_track(self):
        try:
            self.sp.next_track()
            self.tts.play_tts_audio("Próxima música")
        except Exception as e:
            self._handle_playback_error(e)

    def _previous_track(self):
        try:
            self.sp.previous_track()
            self.tts.play_tts_audio("Música anterior")
        except Exception as e:
            self._handle_playback_error(e)

    def _handle_playback_error(self, error: Exception):
        """Handle error during playback."""

        if hasattr(error, 'http_status') and error.http_status == 403:
            print("Erro HTTP 403: Ação não permitida.")
        else:
            print(f"Erro durante a reprodução: {error}")

    def repeat(self, text: str):
        """Control repeat and shuffle of Spotify music."""

        if 'repetir' in text and 'musica' in text or 'faixa' in text:
            self._set_repeat('track')
            self.tts.play_tts_audio("Repetindo música")

        elif 'repetir' in text and 'playlist' in text:
            self._set_repeat('context')
            self.tts.play_tts_audio("Repetindo playlist")

        elif 'repetir' in text and 'desligar' in text:
            self._set_repeat('off')
            self.tts.play_tts_audio("Repetição desligada")

        elif 'aleatorio' in text and 'desligar' in text or 'desativar' in text:
            self._toggle_shuffle(False)
            self.tts.play_tts_audio("Reprodução aleatória desativada")

        elif 'aleatorio' in text:
            self._toggle_shuffle(True)
            self.tts.play_tts_audio("Reprodução aleatória ativada")
    def _set_repeat(self, mode: str):
        try:
            self.sp.repeat(mode)
        except Exception as e:
            print(f"Erro ao definir repetição: {e}")

    def _toggle_shuffle(self, shuffle: bool):
        try:
            self.sp.shuffle(shuffle)
        except Exception as e:
            print(f"Erro ao definir shuffle: {e}")

    def get_info(self, text: str) -> dict:
        """get information about the current music."""

        info = None
        if 'musica, atual' in text or 'informação' in text or 'informações' in text:
            info = self.search_info(self.sp.current_playback(), 'single')
            print(info)
            self.tts.play_tts_audio(f"A música atual é {info['music_name']} de {info['artist']}, do álbum {info['album_name']}, lançado em {info['release_date']}")
            self.tts.play_tts_audio("Deseja salvar essa música?")
            
            user_input = recognizer().wait_question()
            if 'sim' in user_input:
                self.sp.current_user_saved_tracks_add(tracks=[info['uri']])
                self.tts.play_tts_audio("Música salva com sucesso")
            return info

    def search_music(self, text: str):
        """Search 5 songs based on user input"""

        if 'procurar' in text or 'buscar' in text:
            query = text.replace('procurar', '').replace('buscar', '').replace('musica', '').strip()
            print('procurando: ' + query)
            self.tts.play_tts_audio(f"Procurando por {query}")
            self._search_and_play(query)

    def _search_and_play(self, query: str): 
        """informs 5 songs and question for the user for play or not."""

        search_results = self.sp.search(query, limit=5)
        for i in range(5):   
            music_info = self.search_info(search_results, 'multiple', index=i)
            print(music_info)
            self.tts.play_tts_audio(f"{i+1} - {music_info['music_name']} de {music_info['artist']}, do álbum {music_info['album_name']}")
            self.tts.play_tts_audio("Deseja tocar essa música?")
            text = recognizer().wait_question()
            if 'tocar' in text or 'sim' in text:
                self.sp.start_playback(music_info['uri'])
                print('Tocando: ' + music_info['music_name'])
                self.tts.play_tts_audio(f"Tocando {music_info['music_name']}")
                return
            if 'passar' in text or 'proxima' in text or 'pular' in text or 'não' in text:
                self.tts.play_tts_audio("Procurando outra música")
        self.tts.play_tts_audio("Nenhuma música encontrada")
    
    def play_private_playlist(self, user_input: str):
        """Search and play private playlist """

        if 'playlist' in user_input:
            user_input = user_input.replace('playlist', '').strip()
            print('procurando playlist')
            playlist = self.sp.current_user_playlists()

            for item in playlist['items']:
                if item['name'].lower() in user_input.lower():
                    print(item['name'] + item['uri'])
                    self.sp.start_playback(context_uri=item['uri'])
                    self.tts.play_tts_audio(f"Tocando playlist {item['name']}")
                    return


    def volume(self, user_input: str):
        """Set volume of Spotify music."""

        if 'aumentar' in user_input and 'volume' in user_input:
            volume = self.sp.devices()['devices'][0]['volume_percent'] + 10
            self.sp.volume(volume)
            self.tts.play_tts_audio(f"Volume aumentado para {volume}")

        elif 'diminuir' in user_input and 'volume' in user_input:
            volume = self.sp.devices()['devices'][0]['volume_percent'] - 10
            self.sp.volume(volume)
            self.tts.play_tts_audio(f"Volume diminuído para {volume}")
        
        elif 'volume' in user_input:
            volume = ''.join([char for char in user_input if char.isdigit()])
            try:
                self.sp.volume(int(volume))
            except Exception as e:
                print(f"Erro ao ajustar volume: {e}")
                self.tts.play_tts_audio("Erro ao ajustar volume, Tente novamente com um valor entre 0 e 100")
            self.tts.play_tts_audio(f"Volume ajustado para {volume}")
        
        

    def treat_cmd(self, text: str):
        """Processa os comandos de controle de reprodução e busca de músicas."""

        text = text.lower()
        self.repeat(text)
        self.get_info(text)
        self.search_music(text)
        self.volume(text)
        self.play_private_playlist(text)
        self.control_playback(text)


if __name__ == '__main__':
    controller = SpotifyController()
    print(controller.sp.devices())
