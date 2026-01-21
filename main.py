import pygame
import random
import os

USAR_IMAGENS = True  

ARQUIVOS_IMAGENS = [
    "foto1.jpeg","foto2.jpg","foto3.jpg","foto4.jpg","foto5.jpg",
    "foto6.jpg","foto7.jpeg","foto8.jpg","foto9.jpeg","foto10.jpg",
    "foto11.jpg","foto12.jpg","foto13.jpg","foto14.jpg","foto15.jpg",
    "foto16.jpeg","foto17.jpeg","foto18.jpg","foto19.jpg","foto20.jpg",
    "foto21.jpg","foto22.jpg","foto23.jpg","foto24.jpg","foto25.jpg",
]

EMOJIS = ["🍎","🍊","🍋","🍌","🍇","🍓","🍑","🍒"]

pygame.init()

LARGURA = 1620  
ALTURA = 920
TAMANHO_CARTA = 140
ESPACO = 20

BRANCO = (255,255,255)
PRETO = (0,0,0)
CINZA = (200,200,200)
AZUL = (100,150,255)
VERDE = (100,255,100)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Memória")

fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 72)

TELA_INICIAL = 0
JOGANDO = 1
TRANSICAO_FASE = 2
FIM = 3

estado_jogo = TELA_INICIAL

fase = 1
pares_por_fase = {1: 6, 2: 12, 3: 25}

pontos = 0
tentativas = 0
pares_encontrados = 0

imagens_carregadas = {}
imagens_ok = False

if USAR_IMAGENS:
    pasta_imagens = "imagens"
    if os.path.exists(pasta_imagens):
        for i, arquivo in enumerate(ARQUIVOS_IMAGENS):
            try:
                img = pygame.image.load(os.path.join(pasta_imagens, arquivo))
                imagens_carregadas[i] = pygame.transform.scale(img, (100, 100))
            except:
                imagens_carregadas[i] = None
        imagens_ok = True
    else:
        USAR_IMAGENS = False

def criar_cartas(qtd_pares):
    cartas = []

    if USAR_IMAGENS and imagens_ok:
        valores = list(range(qtd_pares)) * 2
    else:
        valores = EMOJIS[:qtd_pares] * 2

    random.shuffle(valores)

    if qtd_pares <= 6:
        colunas = 4
    elif qtd_pares <= 12:
        colunas = 6
    else:
        colunas = 10

    linhas = (len(valores) + colunas - 1) // colunas

    largura_grade = colunas * TAMANHO_CARTA + (colunas - 1) * ESPACO
    altura_grade = linhas * TAMANHO_CARTA + (linhas - 1) * ESPACO

    inicio_x = (LARGURA - largura_grade) // 2
    inicio_y = 160

    pos = 0
    for linha in range(linhas):
        for coluna in range(colunas):
            if pos >= len(valores):
                break

            x = inicio_x + coluna * (TAMANHO_CARTA + ESPACO)
            y = inicio_y + linha * (TAMANHO_CARTA + ESPACO)

            cartas.append({
                'valor': valores[pos],
                'x': x,
                'y': y,
                'virada': False,
                'encontrada': False
            })
            pos += 1

    return cartas

cartas = criar_cartas(pares_por_fase[fase])

carta_selecionada = None
segunda_carta = None
pode_clicar = True
tempo_espera = 0

rodando = True
relogio = pygame.time.Clock()

while rodando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado_jogo == TELA_INICIAL and evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos
            if 660 < mx < 960 and 420 < my < 510:
                estado_jogo = JOGANDO

        if estado_jogo == JOGANDO and evento.type == pygame.MOUSEBUTTONDOWN and pode_clicar:
            mx, my = evento.pos
            for carta in cartas:
                if carta['x'] < mx < carta['x'] + TAMANHO_CARTA and carta['y'] < my < carta['y'] + TAMANHO_CARTA:
                    if not carta['virada'] and not carta['encontrada']:
                        carta['virada'] = True
                        if carta_selecionada is None:
                            carta_selecionada = carta
                        else:
                            segunda_carta = carta
                            pode_clicar = False
                            tentativas += 1
                            tempo_espera = pygame.time.get_ticks()

        if estado_jogo == TRANSICAO_FASE and evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos
            if 660 < mx < 960 and 450 < my < 530:
                fase += 1
                if fase > 3:
                    estado_jogo = FIM
                else:
                    cartas = criar_cartas(pares_por_fase[fase])
                    pares_encontrados = 0
                    carta_selecionada = None
                    segunda_carta = None
                    pode_clicar = True
                    estado_jogo = JOGANDO

    if segunda_carta:
        if pygame.time.get_ticks() - tempo_espera > 800:
            if carta_selecionada['valor'] == segunda_carta['valor']:
                carta_selecionada['encontrada'] = True
                segunda_carta['encontrada'] = True
                pontos += 10
                pares_encontrados += 1
            else:
                carta_selecionada['virada'] = False
                segunda_carta['virada'] = False

            carta_selecionada = None
            segunda_carta = None
            pode_clicar = True

    if pares_encontrados == pares_por_fase[fase]:
        estado_jogo = TRANSICAO_FASE

    tela.fill(BRANCO)

    if estado_jogo == TELA_INICIAL:
        tela.fill((240,245,255))
        titulo = fonte_grande.render("JOGUINHO DA MEMORINHA", True, (50,50,120))
        subtitulo = fonte.render("Cuidado com o amigo que ao vivo brilha, na foto assusta!", True, PRETO)

        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 220))
        tela.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 300))

        pygame.draw.rect(tela, AZUL, (660, 420, 300, 90), border_radius=15)
        pygame.draw.rect(tela, PRETO, (660, 420, 300, 90), 3, border_radius=15)

        texto = fonte_grande.render("JOGAR", True, BRANCO)
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 445))

    elif estado_jogo == JOGANDO:
        tela.blit(fonte.render(f"Fase {fase}", True, PRETO), (20, 20))
        tela.blit(fonte.render(f"Pontos: {pontos}", True, PRETO), (160, 20))

        for carta in cartas:
            rect = pygame.Rect(carta['x'], carta['y'], TAMANHO_CARTA, TAMANHO_CARTA)

            if carta['virada'] or carta['encontrada']:
                pygame.draw.rect(tela, AZUL, rect)
                pygame.draw.rect(tela, PRETO, rect, 2)

                if USAR_IMAGENS and imagens_ok:
                    img = imagens_carregadas[carta['valor']]
                    if img:
                        tela.blit(img, (carta['x'] + 20, carta['y'] + 20))
                else:
                    txt = fonte_grande.render(str(carta['valor']), True, BRANCO)
                    tela.blit(txt, txt.get_rect(center=rect.center))
            else:
                pygame.draw.rect(tela, CINZA, rect)
                pygame.draw.rect(tela, PRETO, rect, 2)

    elif estado_jogo == TRANSICAO_FASE:
        tela.fill((230,255,230))
        msg = fonte_grande.render(f"FASE {fase} CONCLUÍDA!", True, VERDE)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, 300))

        info = fonte.render(f"Pontos: {pontos}", True, PRETO)
        tela.blit(info, (LARGURA//2 - info.get_width()//2, 380))

        pygame.draw.rect(tela, AZUL, (660, 450, 300, 80), border_radius=15)
        texto = fonte.render("CONTINUAR", True, BRANCO)
        tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 475))

    elif estado_jogo == FIM:
        tela.fill(BRANCO)
        fim = fonte_grande.render("VOCÊ FINALIZOU O JOGO!", True, VERDE)
        tela.blit(fim, (LARGURA//2 - fim.get_width()//2, 350))

        final = fonte.render(f"Pontos finais: {pontos}", True, PRETO)
        tela.blit(final, (LARGURA//2 - final.get_width()//2, 430))

    pygame.display.flip()

pygame.quit()