from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class SystemVolume:
    def __init__(self):
        # Inicializa acesso ao volume do sistema
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def get_volume_percent(self) -> int:
        """Retorna o volume atual do sistema como porcentagem (0 a 100)."""
        return int(self.volume.GetMasterVolumeLevelScalar() * 100)

    def set_volume_percent(self, percent: int):
        """Define o volume do sistema. Valor deve estar entre 0 e 100."""
        scalar = max(0.0, min(1.0, percent / 100))
        self.volume.SetMasterVolumeLevelScalar(scalar, None)

    def get_volume_db(self) -> float:
        """Retorna o volume em decibéis (valores negativos)."""
        return self.volume.GetMasterVolumeLevel()

# ==============================
# Exemplo de uso
# ==============================
if __name__ == "__main__":
    vol = SystemVolume()

    print(f"Volume atual: {vol.get_volume_percent()}%")
    print(f"Volume em dB: {vol.get_volume_db():.2f} dB")

    novo_volume = 25
    print(f"Definindo volume para {novo_volume}%...")
    vol.set_volume_percent(novo_volume)
    print(f"Novo volume: {vol.get_volume_percent()}%")
