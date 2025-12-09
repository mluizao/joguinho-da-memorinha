import pygame
import random
import os

# ============================================
# CONFIGURAÇÕES - MUDE AQUI!
# ============================================

USAR_IMAGENS = True  # Mude para True para usar imagens

ARQUIVOS_IMAGENS = [
    "foto1.jpeg",
    "foto2.jpg", 
    "foto3.jpg",
    "foto4.jpg",
    "foto5.jpg",
    "foto6.jpg",
    "foto7.jpeg",
    "foto8.jpg",
    "foto9.jpeg",
    "foto10.jpg",
    "foto11.jpg",
    "foto12.jpg",
    "foto13.jpg",
    "foto14.jpg",
    "foto15.jpg",
    "foto16.jpeg",
    "foto17.jpeg",
    "foto18.jpg",
    "foto19.jpg",
    "foto20.jpg",
    "foto21.jpg",
    "foto22.jpg",
    "foto23.jpg",
    "foto24.jpg",
    "foto25.jpg",
]

# Se não usar imagens, usa emojis
EMOJIS = ["🍎", "🍊", "🍋", "🍌", "🍇", "🍓", "🍑", "🍒"]

# ============================================

# Inicializa pygame
pygame.init()

# Tamanhos
LARGURA = 1620  # ERRO 1: tinha vírgula aqui!
ALTURA = 920
TAMANHO_CARTA = 140
ESPACO = 20

# Cores simples
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
AZUL = (100, 150, 255)
VERDE = (100, 255, 100)
VERMELHO = (255, 100, 100)

# Cria tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Memoria")

# Fonte
fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 72)

# Variáveis do jogo
pontos = 0
tentativas = 0
pares_encontrados = 0

# Carrega imagens se necessário
imagens_carregadas = {}
imagens_ok = False

if USAR_IMAGENS:
    print("\n=== CARREGANDO IMAGENS ===")
    print(f"Pasta atual: {os.getcwd()}")
    print(f"Procurando pasta 'imagens'...")
    
    pasta_imagens = "imagens"
    
    # Verifica se a pasta existe
    if os.path.exists(pasta_imagens):
        print(f"✓ Pasta '{pasta_imagens}' encontrada!")
        print(f"\nArquivos na pasta:")
        arquivos_na_pasta = os.listdir(pasta_imagens)
        for arq in arquivos_na_pasta:
            print(f"  - {arq}")
        print()
    else:
        print(f"✗ ERRO: Pasta '{pasta_imagens}' não encontrada!")
        print(f"Crie a pasta 'imagens' no mesmo local do arquivo .py")
        USAR_IMAGENS = False
    
    if USAR_IMAGENS:
        imagens_carregadas_count = 0
        for i, arquivo in enumerate(ARQUIVOS_IMAGENS):
            try:
                caminho = os.path.join(pasta_imagens, arquivo)
                print(f"Tentando carregar: {caminho}")
                
                if not os.path.exists(caminho):
                    print(f"  ✗ Arquivo não encontrado: {arquivo}")
                    imagens_carregadas[i] = None
                    continue
                
                img = pygame.image.load(caminho)
                # Redimensiona mantendo proporção
                img = pygame.transform.scale(img, (100, 100))
                imagens_carregadas[i] = img
                imagens_carregadas_count += 1
                print(f"  ✓ Carregada com sucesso!")
                
            except Exception as e:
                print(f"  ✗ Erro ao carregar {arquivo}: {str(e)}")
                imagens_carregadas[i] = None
        
        print(f"\n{imagens_carregadas_count} de {len(ARQUIVOS_IMAGENS)} imagens carregadas com sucesso!")
        
        if imagens_carregadas_count >= 25:  # ERRO 2: verificava 8 mas precisa 25!
            imagens_ok = True
            print("✓ Jogo pronto para usar imagens!\n")
        else:
            print("✗ Não foram carregadas imagens suficientes. Usando emojis.\n")
            USAR_IMAGENS = False

# Cria cartas
cartas = []
if USAR_IMAGENS and imagens_ok:
    valores = list(range(25)) * 2  # 0,1,2...24 duas vezes = 50 cartas
    print("Modo: IMAGENS")
else:
    valores = EMOJIS * 2  # cada emoji duas vezes
    print("Modo: EMOJIS")

random.shuffle(valores)

# Posiciona cartas em grade 5x10 (5 colunas, 10 linhas)
posicao = 0
for linha in range(5):  # ERRO 3: era 5, mas 5x5=25, precisa 5x10=50!
    for coluna in range(10):
        x = coluna * (TAMANHO_CARTA + ESPACO) + ESPACO
        y = linha * (TAMANHO_CARTA + ESPACO) + ESPACO + 100
        
        carta = {
            'valor': valores[posicao],
            'x': x,
            'y': y,
            'virada': False,
            'encontrada': False
        }
        cartas.append(carta)
        posicao += 1

# Estado do jogo
carta_selecionada = None
segunda_carta = None
pode_clicar = True
tempo_espera = 0

print("=== INICIANDO JOGO ===\n")

# Loop principal
rodando = True
relogio = pygame.time.Clock()

while rodando:
    relogio.tick(60)
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and pode_clicar:
            mouse_x, mouse_y = evento.pos
            
            # Verifica qual carta foi clicada
            for carta in cartas:
                if (carta['x'] < mouse_x < carta['x'] + TAMANHO_CARTA and
                    carta['y'] < mouse_y < carta['y'] + TAMANHO_CARTA and
                    not carta['virada'] and not carta['encontrada']):
                    
                    carta['virada'] = True
                    
                    if carta_selecionada is None:
                        carta_selecionada = carta
                    else:
                        segunda_carta = carta
                        pode_clicar = False
                        tentativas += 1
                        tempo_espera = pygame.time.get_ticks()
    
    # Verifica par
    if segunda_carta is not None:
        tempo_atual = pygame.time.get_ticks()
        
        if tempo_atual - tempo_espera > 1000:  # Espera 1 segundo
            if carta_selecionada['valor'] == segunda_carta['valor']:
                # Acertou!
                carta_selecionada['encontrada'] = True
                segunda_carta['encontrada'] = True
                pontos += 10
                pares_encontrados += 1
            else:
                # Errou
                carta_selecionada['virada'] = False
                segunda_carta['virada'] = False
            
            carta_selecionada = None
            segunda_carta = None
            pode_clicar = True
    
    # Desenha tudo
    tela.fill(BRANCO)
    
    # Desenha info no topo
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    texto_tentativas = fonte.render(f"Tentativas: {tentativas}", True, PRETO)
    texto_pares = fonte.render(f"Pares: {pares_encontrados}/25", True, PRETO)  # ERRO 4: era /8!
    
    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_tentativas, (240, 20))
    tela.blit(texto_pares, (520, 20))
    
    # Desenha linha
    pygame.draw.line(tela, PRETO, (0, 80), (LARGURA, 80), 2)
    
    # Desenha cartas
    for carta in cartas:
        # Retangulo da carta
        rect = pygame.Rect(carta['x'], carta['y'], TAMANHO_CARTA, TAMANHO_CARTA)
        
        if carta['encontrada']:
            pygame.draw.rect(tela, VERDE, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)
        elif carta['virada']:
            pygame.draw.rect(tela, AZUL, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)
            
            # Mostra conteudo
            if USAR_IMAGENS and imagens_ok:
                valor_carta = carta['valor']
                if valor_carta in imagens_carregadas and imagens_carregadas[valor_carta] is not None:
                    img_x = carta['x'] + (TAMANHO_CARTA - 100) // 2
                    img_y = carta['y'] + (TAMANHO_CARTA - 100) // 2
                    tela.blit(imagens_carregadas[valor_carta], (img_x, img_y))
                else:
                    # Fallback para numero
                    texto = fonte_grande.render(str(valor_carta), True, BRANCO)
                    texto_rect = texto.get_rect(center=rect.center)
                    tela.blit(texto, texto_rect)
            else:
                # Mostra emoji
                texto = fonte_grande.render(carta['valor'], True, BRANCO)
                texto_rect = texto.get_rect(center=rect.center)
                tela.blit(texto, texto_rect)
        else:
            # Carta virada pra baixo
            pygame.draw.rect(tela, CINZA, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)
            
            # Desenha um "?" 
            texto = fonte_grande.render("?", True, PRETO)
            texto_rect = texto.get_rect(center=rect.center)
            tela.blit(texto, texto_rect)
    
    # Verifica se ganhou
    if pares_encontrados == 25:  # ERRO 5: era 8!
        # Tela de vitoria
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(BRANCO)
        overlay.set_alpha(200)
        tela.blit(overlay, (0, 0))
        
        texto_vitoria = fonte_grande.render("VOCE GANHOU!", True, VERDE)
        texto_rect = texto_vitoria.get_rect(center=(LARGURA//2, ALTURA//2 - 50))
        tela.blit(texto_vitoria, texto_rect)
        
        texto_final = fonte.render(f"Pontos finais: {pontos}", True, PRETO)
        texto_rect2 = texto_final.get_rect(center=(LARGURA//2, ALTURA//2 + 20))
        tela.blit(texto_final, texto_rect2)
        
        texto_tent = fonte.render(f"Em {tentativas} tentativas", True, PRETO)
        texto_rect3 = texto_tent.get_rect(center=(LARGURA//2, ALTURA//2 + 60))
        tela.blit(texto_tent, texto_rect3)
    
    pygame.display.flip()

pygame.quit()