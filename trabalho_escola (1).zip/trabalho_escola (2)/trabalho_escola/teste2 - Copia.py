
#! Ta instavel ( eu acho)
#! Eterno 2pac
import pygame
import os
from pygame.locals import *
from sys import exit
from random import randint, choice

pygame.init()

caminho_base = os.path.dirname(os.path.abspath(__file__))

# Função para carregar arquivos de forma dinâmica
def carregar_arquivo(caminho_relativo):
    return os.path.join(caminho_base, caminho_relativo)

#? Config tela
largura = 900
altura = 900
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')

#? Cores
pedracolor = (125, 127, 125)
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (200, 0, 0)

#? Fonte
fonte_menu = pygame.font.SysFont('comicsans', 50)
fonte = pygame.font.SysFont('comicsans', 40, True, False)

#? Soundtrack
try:
    pygame.mixer.music.load(carregar_arquivo('sons/Soundtrack(2).mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.25)
except pygame.error as e:
    print(f"Erro ao carregar a música: {e}")

#? Sons de colisão
try:
    sounds = [
        pygame.mixer.Sound(carregar_arquivo('sons/soundeat1.mp3')),
        pygame.mixer.Sound(carregar_arquivo('sons/soundeat2.mp3'))
    ]
except pygame.error as e:
    print(f"Erro ao carregar um dos sons: {e}")

#? Carregar imagens
imgobstaculo = pygame.image.load(carregar_arquivo('backg/obstaculoimg.png')).convert_alpha()
imgmaca = pygame.image.load(carregar_arquivo('backg/macaimg.png')).convert_alpha()
imgpedra = pygame.image.load(carregar_arquivo('snakee/pedra2.png')).convert_alpha()
imagem_fundo = pygame.image.load(carregar_arquivo('backg/bc1.png')).convert()
imagem_cabeca = pygame.image.load(carregar_arquivo('snakee/cabecac.png')).convert_alpha()
imagem_corpo = pygame.image.load(carregar_arquivo('snakee/corpoc.png')).convert_alpha()
imagem_rabo = pygame.image.load(carregar_arquivo('snakee/raboc.png')).convert_alpha()

#? Img cobra (Sim, isto e mt idiota, mas vai funcionar por enquanto 15/08/24)
comprimento_pixel = 20
tamanho_segmento = (comprimento_pixel, comprimento_pixel)
imagem_cabeca = pygame.transform.scale(imagem_cabeca, tamanho_segmento)
imagem_corpo = pygame.transform.scale(imagem_corpo, tamanho_segmento)
imagem_rabo = pygame.transform.scale(imagem_rabo, tamanho_segmento)
imgobstaculo = pygame.transform.scale(imgobstaculo, (80, 20)) 
imgmaca = pygame.transform.scale(imgmaca, (20, 20))

#? Variáveis iniciais
velocidade = 5
xcontrole = velocidade
ycontrole = 0
xcobra = largura / 2
ycobra = altura / 2
xmaca = randint(100 , 700)
ymaca = randint(100 , 700)
pontos = 0
comprimentoinicial = 3
listacobra = []
obstaculos = [(randint(100, 700), randint(100, 700))]

morte = False
relogio = pygame.time.Clock()

#? Sim, isso e idiota, mas vai funcionar por enquanto
posicoes_pedra = [
    (235, 237),  #? Canto sup esquerdo
    (613, 237),  #? Canto sup direito
    (235, 615),  #? Canto inf esquerdo
    (613, 615)   #? Canto inf direito
]

def rotacionar_cabeca(direcao_x, direcao_y):
    if direcao_x > 0:  #? Indo para a direita
        return pygame.transform.rotate(imagem_cabeca, 270)
    elif direcao_x < 0:  #? Indo para a esquerda
        return pygame.transform.rotate(imagem_cabeca, 90)
    elif direcao_y > 0:  #? Indo para baixo
        return pygame.transform.rotate(imagem_cabeca, 180)
    else:  #? Indo para cima (ou se não houver movimento, manter para cima)
        return pygame.transform.rotate(imagem_cabeca, 0)

#? Funções do jogo
def desenhar_cobra(listacobra):
    for index, (x, y) in enumerate(listacobra):
        if index == 0:
            tela.blit(imagem_rabo, (x, y))
        elif index == len(listacobra) - 1:
            tela.blit(imagem_cabeca, (x, y))
        else:
            tela.blit(imagem_corpo, (x, y))

def desenhar_pedras():
    for pedra_pos in posicoes_pedra:
        tela.blit(imgpedra, pedra_pos)

def exibir_game_over():
    fonte2 = pygame.font.SysFont('arial', 30, True, True)
    mensagem2 = "Game Over, aperte E para reiniciar"
    textoformatado2 = fonte2.render(mensagem2, True, (0, 0, 0))
    tela.fill((170, 0, 0))
    tela.blit(textoformatado2, (largura // 4, altura // 2))
    pygame.display.update()

def reiniciar():
    global pontos, comprimentoinicial, xcobra, ycobra, listacobra, xmaca, ymaca, morte, obstaculos, velocidade
    pontos = 0
    comprimentoinicial = 3
    xcobra = largura / 2
    ycobra = altura / 2
    listacobra = []
    xmaca = randint(100, 700)
    ymaca = randint(100, 700)
    obstaculos = [(randint(100, 700), randint(100, 700))]
    morte = False
    velocidade = 5

def play_collision_sound():
    sound_to_play = choice(sounds)
    sound_to_play.play()

def adicionar_obstaculo(lista):
    while True:
        x = randint(100, 700)
        y = randint(100, 700)
        distancia_valida = True
        for ox, oy in lista + listacobra:  #? verificar a cobra
            if abs(ox - x) < 50 and abs(oy - y) < 50:
                distancia_valida = False
                break
        if abs(x - xmaca) < 50 and abs(y - ymaca) < 50:  #? verificar maçã
            distancia_valida = False
        for px, py in posicoes_pedra:
            if abs(px - x) < 50 and abs(py - y) < 50:
                distancia_valida = False
                break            
            
        if distancia_valida:
            lista.append((x, y))
            break

def teletransporte_cobra():
    global xcobra, ycobra
    if xcobra < 0:
        xcobra = largura
    elif xcobra > largura:
        xcobra = 0
    if ycobra < 0:
        ycobra = altura
    elif ycobra > altura:
        ycobra = 0

direcao_atual = (xcontrole, ycontrole)

#? Loop principal do jogo
while True:
    relogio.tick(30)
    tela.blit(imagem_fundo, (0, 0))

    #? Verificar colisão com pedras
    for pedra_pos in posicoes_pedra:
        pedra_rect = pygame.Rect(pedra_pos[0], pedra_pos[1], 20, 20)
        if pygame.Rect(xcobra, ycobra, comprimento_pixel, comprimento_pixel).colliderect(pedra_rect):
            play_collision_sound()
            morte = True

    mensagem = f'Pontos: {pontos}'
    textoformatado = fonte.render(mensagem, True, (199, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a and xcontrole != velocidade:
                xcontrole = -velocidade
                ycontrole = 0
            if event.key == K_d and xcontrole != -velocidade:
                xcontrole = velocidade
                ycontrole = 0
            if event.key == K_s and ycontrole != -velocidade:
                xcontrole = 0
                ycontrole = velocidade
            if event.key == K_w and ycontrole != velocidade:
                xcontrole = 0
                ycontrole = -velocidade
            if event.key == K_e and morte:
                reiniciar()
            if event.key == K_a and xcontrole != velocidade:
                xcontrole = -velocidade
                ycontrole = 0
            if event.key == K_d and xcontrole != -velocidade:
                xcontrole = velocidade
                ycontrole = 0
            if event.key == K_s and ycontrole != -velocidade:
                xcontrole = 0
                ycontrole = velocidade
            if event.key == K_w and ycontrole != velocidade:
                xcontrole = 0
                ycontrole = -velocidade
            if event.key == K_e and morte:
                reiniciar()

    desenhar_pedras()  #? Desenhar as pedras

    cobra = pygame.Rect(xcobra, ycobra, comprimento_pixel, comprimento_pixel)
    tela.blit(imgmaca, (xmaca, ymaca))

    #? Verificar colisão com a maçã
    maca_rect = pygame.Rect(xmaca, ymaca, comprimento_pixel, comprimento_pixel)
    if cobra.colliderect(maca_rect):
        play_collision_sound()
        xmaca = randint(100, 700)
        ymaca = randint(100, 700)
        pontos += 1
        if pontos % 5 == 0:  #? Aumentar velocidade a cada 5 pontos-
            velocidade += 2
        comprimentoinicial += 3
        adicionar_obstaculo(obstaculos)

    #? Obstáculos e verificar colisão
    for xobstaculo, yobstaculo in obstaculos:
        tela.blit(imgobstaculo, (xobstaculo, yobstaculo))
        obstaculo_rect = pygame.Rect(xobstaculo, yobstaculo, imgobstaculo.get_width(), imgobstaculo.get_height())
        if cobra.colliderect(obstaculo_rect):
            play_collision_sound()
            morte = True

    cabeca = [xcobra, ycobra]
    listacabeca = listacobra[:]
    listacabeca.append(cabeca)

    if len(listacobra) > comprimentoinicial:
        del listacobra[0]

    if cabeca in listacobra:
        play_collision_sound()
        morte = True

    #? Exibir Game Over e pausar até que pressione E
    if morte:
        exibir_game_over()
        while morte:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_e:
                    reiniciar()
            pygame.display.update()
        continue  #? Pular o restante do loop se o jogo acabou

    listacobra.append([xcobra, ycobra])

    teletransporte_cobra()
    desenhar_cobra(listacobra)
    tela.blit(textoformatado, (40, 40))
    pygame.display.update()

    #? Movimentação da cobra
    xcobra += xcontrole
    ycobra += ycontrole
