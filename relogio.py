import pygame
import time
import ctypes
import queue

pygame.init()

def turn_off_monitor():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)

def turn_on_monitor():
    ctypes.windll.user32.mouse_event(1, 0, 0, 0, 0)

def start_clock(command_queue):
    """
    Exibe o relógio digital com a capacidade de receber comandos através da fila.
    """
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Modo tela cheia
    pygame.display.set_caption("Relógio Digital Minimalista")
    black = (0, 0, 0)  # Cor preta para o fundo
    red = (255, 0, 0)  # Cor vermelha para o texto
    white = (255, 255, 255)  # Cor branca para mensagens
    font = pygame.font.Font(None, 150)  # Fonte do relógio
    message_font = pygame.font.Font(None, 60)  # Fonte para mensagens abaixo do relógio

    current_message = ""  # Mensagem que ficará abaixo do relógio
    display_clock = True  # Flag para controle do modo relógio

    running = True
    monitor_on = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False  # Saída do programa quando ESC é pressionado
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                turn_off_monitor()
                monitor_on = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not monitor_on:
                turn_on_monitor()
                monitor_on = True

        # Checar se há comandos na fila
        try:
            command = command_queue.get_nowait()  # Não bloqueia se não houver comandos
            if command.startswith("message:"):
                current_message = command[len("message:"):]  # Exibe a mensagem recebida
            match command:
                case "desligar_tela":
                    turn_off_monitor()
                    monitor_on = False
                case "mostrar_relogio":
                    display_clock = True  # Mostrar o relógio
                case "esconder_relogio":
                    display_clock = False  # Esconder o relógio
        except queue.Empty:
            pass

        if monitor_on and display_clock:
            screen.fill(black)
            current_time = time.strftime("%d/%m/%Y  %H:%M")  # Formato do relógio
            text = font.render(current_time, True, red)
            text_rect = text.get_rect(center=screen.get_rect().center)  # Centralizar texto
            screen.blit(text, text_rect)

            if current_message:
                message_text = message_font.render(current_message, True, white)
                message_rect = message_text.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery + 100))
                screen.blit(message_text, message_rect)
            pygame.display.flip()

        pygame.time.delay(100)
    pygame.quit()