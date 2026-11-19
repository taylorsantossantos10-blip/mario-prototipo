import pygame, random, os
pygame.init()
FUNDO = pygame.image.load("fundo.png")
INICIO = pygame.image.load("inicio.png")
INICIO = pygame.transform.scale(INICIO, (800,480))
PLATAFORMA = pygame.image.load("plataforma.png")
FUNDO = pygame.image.load("fundo.png")


T = pygame.display.set_mode((800, 480))

# BOTAO PLAY - tamanho pequeno certo
try:
    botao_play_img = pygame.image.load("botao_play_limpo.png")
except:
    botao_play_img = pygame.image.load("botao_play.png")
botao_play_img = pygame.transform.scale(botao_play_img, (110, 45))

FUNDO = pygame.transform.scale(FUNDO, T.get_size())
F = pygame.font.SysFont(None, 32)
G = pygame.font.SysFont(None, 50)
estado = "menu"
mario = None
if os.path.exists("mario.png"):
    mario = pygame.image.load("mario.png")
    mario.set_colorkey((0, 0, 0))
    mario = pygame.transform.scale(mario, (60, 85))
def desenha_mario(x, y):
    if mario:
        T.blit(mario, (x, y)); return
    pygame.draw.rect(T, (255,0,0), (x+5, y, 50, 18), border_radius=8)
    pygame.draw.rect(T, (255,200,150), (x+8, y+18, 44, 28))
    pygame.draw.rect(T, (60,30,0), (x+15, y+35, 30, 8))
    pygame.draw.rect(T, (255,0,0), (x+2, y+46, 56, 20))
    pygame.draw.rect(T, (0,80,255), (x+10, y+46, 40, 35))
    pygame.draw.rect(T, (120,60,0), (x+5, y+78, 20, 12))
    pygame.draw.rect(T, (120,60,0), (x+35, y+78, 20, 12))
def novo_chunk(wx):
    m=[]; im=[]
    for i in range(random.randint(1,3)): m.append([wx+random.randint(50,350),280])
    if random.random()<0.7: im.append([wx+random.randint(100,300),350])
    return {"wx":wx,"moedas":m,"inim":im}
def reset():
    global px,py,vy,vida,pts,dist,chunks,tiros,cam,vel_andar,nuvens
    px,py,vy,vida,pts,dist,tiros,cam = 200,320,0,3,0,0,[],0
    vel_andar = 9
    chunks=[novo_chunk(i*400) for i in range(5)]
    nuvens=[[random.randint(0,800),random.randint(20,120)] for _ in range(6)]
reset()
b_jogar=botao_play_img.get_rect(center=(400,240))
b_continuar=pygame.Rect(300,240,200,60)
b_again=pygame.Rect(300,280,200,60)
b_menu=pygame.Rect(300,360,200,60)
b_esq=pygame.Rect(20,380,80,70)
b_dir=pygame.Rect(110,380,80,70)
b_pulo=pygame.Rect(580,380,90,70)
b_tiro=pygame.Rect(690,380,90,70)
b_pause=pygame.Rect(700,10,80,35)
clock=pygame.time.Clock()
rodando=True
apertado=""
while rodando:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: rodando=False
        if e.type==pygame.MOUSEBUTTONDOWN:
            if estado=="menu" and b_jogar.collidepoint(e.pos): reset(); estado="jogo"
            elif estado=="gameover" and b_again.collidepoint(e.pos): reset(); estado="jogo"
            elif estado=="gameover" and b_menu.collidepoint(e.pos): estado="menu"
            elif estado=="jogo" and b_pause.collidepoint(e.pos): estado="pause"
            elif estado=="pause" and b_continuar.collidepoint(e.pos): estado="jogo"
            elif estado=="pause" and b_menu.collidepoint(e.pos): estado="menu"
            elif estado=="jogo" and b_pulo.collidepoint(e.pos) and py>=320: vy=-22
            elif estado=="jogo" and b_tiro.collidepoint(e.pos): tiros.append([px+60,py+30])
            elif estado=="jogo" and b_esq.collidepoint(e.pos): apertado="esq"
            elif estado=="jogo" and b_dir.collidepoint(e.pos): apertado="dir"
        if e.type==pygame.MOUSEBUTTONUP: apertado=""
    if estado=="jogo":
        # ANDAR RAPIDO - 13 de velocidade!
        moveu=0
        if apertado=="esq" and px>0: px-=13; moveu=-13
        if apertado=="dir": px+=13; moveu=13
        # CAMERA SEGUE O MARIO - CENARIO SE MOVE!
        cam_alvo = px - 200
        if cam_alvo<0: cam_alvo=0
        cam += (cam_alvo - cam)*0.2
        # PARALLAX: nuvens andam mais devagar que o chao
        for n in nuvens:
            n[0]-=moveu*0.2
            if n[0]<-100: n[0]=850; n[1]=random.randint(20,120)
            if n[0]>850: n[0]=-100
        dist = int(px)
        pts+=1
        # GERA CHUNK NOVO NA FRENTE
        while chunks[-1]["wx"] < cam+1000:
            chunks.append(novo_chunk(chunks[-1]["wx"]+400))
        # APAGA CHUNK ATRAS
        if chunks[0]["wx"] < cam-500:
            chunks.pop(0)
        # PULO RAPIDO E ALTO
        vy+=1.2; py+=vy
        if py>320: py,vy=320,0
        for t in tiros[:]:
            t[0]+=15
            if t[0]>px+600: tiros.remove(t)
        for c in chunks:
            for mm in c["moedas"][:]:
                if abs(px-mm[0])<35 and abs(py-mm[1])<35: pts+=50; c["moedas"].remove(mm)
            for ii in c["inim"][:]:
                if abs(px-ii[0])<40 and abs(py-ii[1])<40:
                    vida-=1; c["inim"].remove(ii)
                    if vida<=0: estado="gameover"
        for t in tiros[:]:
            for c in chunks:
                for ii in c["inim"][:]:
                    if abs(t[0]-ii[0])<30 and abs(t[1]-ii[1])<30:
                        pts+=100; c["inim"].remove(ii)
                        if t in tiros: tiros.remove(t)
    T.blit(INICIO if estado=='menu' else FUNDO, (0, 0))
    if estado == 'menu':
        T.blit(botao_play_img, b_jogar)
    elif estado=="gameover":
        T.blit(G.render("GAME OVER!",True,(255,0,0)),(260,100))
        T.blit(F.render(f"Pontos:{pts} Dist:{dist}",True,(0,0,0)),(230,180))
        for b,txt in [(b_again,"DE NOVO"),(b_menu,"MENU")]:
            pygame.draw.rect(T,(0,150,255),b,border_radius=12)
            T.blit(F.render(txt,True,(255,255,255)),(b.x+40,b.y+15))
    elif estado=="pause":
        T.blit(G.render("PAUSADO",True,(0,0,0)),(300,120))
        for b,txt in [(b_continuar,"CONTINUAR"),(b_menu,"MENU")]:
            pygame.draw.rect(T,(0,150,255),b,border_radius=12)
            T.blit(F.render(txt,True,(255,255,255)),(b.x+30,b.y+15))
    else:
        # NUVENS - PARALLAX
        for n in nuvens:
            pygame.draw.ellipse(T,(255,255,255),(n[0],n[1],90,40))
        # CHUNKS - SE MOVEM COM A CAMERA
        for c in chunks:
            sx = c["wx"] - cam
            T.blit(pygame.transform.scale(PLATAFORMA,(400,85)),(sx,395))
            # grama mais clara em cada chunk pra ver que ta andando
            # grama tirada - agora e o print
            for mm in c["moedas"]:
                pygame.draw.circle(T,(255,215,0),(mm[0]-cam,mm[1]),15)
            for ii in c["inim"]:
                pygame.draw.rect(T,(255,0,0),(ii[0]-cam,ii[1],35,35))
        for t in tiros: pygame.draw.rect(T,(255,255,0),(t[0]-cam, t[1],15,5))
        desenha_mario(px-cam,py)
        for b,txt in [(b_esq,"<"),(b_dir,">"),(b_pulo,"PULAR"),(b_tiro,"TIRO")]:
            pygame.draw.rect(T,(80,80,80),b,border_radius=10)
            T.blit(F.render(txt,True,(255,255,255)),(b.x+10,b.y+25))
        pygame.draw.rect(T,(255,150,0),b_pause,border_radius=8)
        T.blit(F.render("PAUSE",True,(0,0,0)),(705,15))
        T.blit(F.render(f"Pts:{pts} Vida:{vida} Dist:{dist}",True,(0,0,0)),(20,10))
    pygame.display.flip(); clock.tick(30)
pygame.quit()
