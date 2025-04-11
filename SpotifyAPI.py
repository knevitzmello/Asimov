import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAPI():
    def __init__(self, client_id, client_secret, redirect_uri, device_id):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-modify-playback-state user-read-playback-state"
        ))
        self.device_id = device_id

    def find_track(self, track_name):
        results = self.sp.search(q=track_name, type="track", limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            print(f"Track found: {track['name']} by {track['artists'][0]['name']}")
            return track['uri']
        else:
            print(f"Track '{track_name}' not found.")
            return None

    def get_device_id(self, device_name):
        devices = self.sp.devices()
        for device in devices['devices']:
            if device['name'] == device_name:
                return device['id']
        print(f"Device '{device_name}' not found.")
        return None

    def play_music(self, track_name):
        track_uri = self.find_track(track_name)
        if not track_uri:
            return

        device_id = self.get_device_id(self.device_name)
        if not device_id:
            return

        self.sp.transfer_playback(device_id=device_id, force_play=True)
        print(f"Transferência para o dispositivo '{self.device_name}' bem-sucedida.")
        self.sp.start_playback(device_id=device_id, uris=[track_uri])
        print(f"Tocando '{track_name}' no dispositivo '{self.device_name}'.")

    def pause_playback(self):
        self.sp.pause_playback()
        print("Reprodução pausada.")

    def resume_playback(self):
        self.sp.start_playback()
        print("Reprodução retomada.")

    def next_track(self):
        self.sp.next_track()
        print("Faixa seguinte.")

    def previous_track(self):
        self.sp.previous_track()
        print("Faixa anterior.")

    def toggle_repeat(self, mode="off"):
        if mode not in ("off", "track", "context"):
            print("Modo inválido. Use 'off', 'track' ou 'context'.")
            return
        self.sp.repeat(mode)
        print(f"Modo de repetição definido para '{mode}'.")

    def toggle_shuffle(self, state: bool):
        self.sp.shuffle(state)
        print(f"Shuffle {'ativado' if state else 'desativado'}.")

    def process_command(self, command, parameters=None):
        if command == "reproduzir_musica":
            track_name = parameters
            device_name = "MyDevice"
            self.play_music(track_name, device_name)
        elif command == "pausar":
            self.pause_playback()
        elif command == "continuar":
            self.resume_playback()
        elif command == "proxima":
            self.next_track()
        elif command == "anterior":
            self.previous_track()
        elif command == "repetir":
            self.toggle_repeat(parameters or "context")
        elif command == "shuffle":
            self.toggle_shuffle(parameters.lower() == "on")
