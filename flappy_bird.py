import pygame
import random
import os
import time
import neat
pygame.font.init()  # initializează fonturile în pygame

# Constante pentru dimensiunile ferestrei și alte setări
WIN_WIDTH = 600  # lățimea ferestrei de joc
WIN_HEIGHT = 800  # înălțimea ferestrei de joc
FLOOR = 730  # poziția podelei în joc
STAT_FONT = pygame.font.SysFont("comicsans", 50)  # fontul pentru statistici
END_FONT = pygame.font.SysFont("comicsans", 70)  # fontul pentru mesajul de final
DRAW_LINES = False  # decide dacă se desenează liniile pentru rețeaua neuronală

# Inițializarea ferestrei pygame
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # creează fereastra jocului
pygame.display.set_caption("Flappy Bird")  # setează titlul ferestrei

# Încărcarea imaginilor și redimensionarea lor
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())  # imaginea pentru țevi
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))  # imaginea pentru fundal
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]  # imaginile pentru pasăre (animație)
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())  # imaginea pentru baza (podea)

#original_image = pygame.image.load(os.path.join("imgs", "image.png"))
#resized_image = pygame.transform.scale(original_image, (600, 900))

#bird_images = []
#for x in range(1, 4):
#    path = os.path.join("imgs", "bird" + str(x) + ".png")
#    image = pygame.image.load(path)
#    scaled_image = pygame.transform.scale2x(image)
#    bird_images.append(scaled_image)
 
gen = 0  # contor pentru generații

class Bird:
    """
    Clasa Bird reprezintă pasărea din jocul Flappy Bird
    """
    MAX_ROTATION = 25  # rotația maximă a păsării în grade
    IMGS = bird_images  # imaginile pentru animația păsării
    ROT_VEL = 20  # viteza de rotație
    ANIMATION_TIME = 5  # timpul pentru animație

    def __init__(self, x, y):
        """
        Inițializează obiectul pasăre
        :param x: poziția inițială x (int)
        :param y: poziția inițială y (int)
        :return: None
        """
        self.x = x  # poziția x a păsării
        self.y = y  # poziția y a păsării
        self.tilt = 0  # înclinarea păsării în grade
        self.tick_count = 0  # contor pentru calcularea deplasării
        self.vel = 0  # viteza păsării
        self.height = self.y  # înălțimea inițială a păsării
        self.img_count = 0  # contor pentru animație
        self.img = self.IMGS[0]  # imaginea curentă a păsării

    def jump(self):
        """
        Face pasărea să sară
        :return: None
        """
        self.vel = -10.5  # setează viteza negativă (în sus)
        self.tick_count = 0  # resetează contorul de timp
        self.height = self.y  # salvează înălțimea de la care s-a sărit

    def move(self):
        """
        Actualizează poziția păsării în fiecare frame
        :return: None
        """
        self.tick_count += 1  # incrementează contorul de timp

        # Calculează deplasarea folosind ecuația mișcării
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # formula pentru deplasare cu accelerație

        # Limitează viteza terminală
        if displacement >= 16:  # dacă deplasarea depășește 16 pixeli
            displacement = (displacement/abs(displacement)) * 16  # limitează la 16 pixeli, păstrând semnul

        if displacement < 0:  # dacă pasărea se mișcă în sus
            displacement -= 2  # adaugă o deplasare suplimentară în sus

        self.y = self.y + displacement  # actualizează poziția y a păsării

        # Controlează înclinarea păsării
        if displacement < 0 or self.y < self.height + 50:  # dacă pasărea urcă sau este aproape de înălțimea maximă
            if self.tilt < self.MAX_ROTATION:  # verifică dacă nu a atins înclinarea maximă
                self.tilt = self.MAX_ROTATION  # inclină pasărea în sus
        else:  # dacă pasărea cade
            if self.tilt > -90:  # verifică dacă nu a atins înclinarea maximă în jos
                self.tilt -= self.ROT_VEL  # inclină pasărea în jos treptat

    def draw(self, win):
        """
        Desenează pasărea pe ecran cu animație
        :param win: fereastra pygame sau suprafață
        :return: None
        """
        self.img_count += 1  # incrementează contorul pentru animație

        # Animația păsării, ciclează prin cele trei imagini
        if self.img_count <= self.ANIMATION_TIME:  # prima imagine pentru primele ANIMATION_TIME frame-uri
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:  # a doua imagine pentru următoarele ANIMATION_TIME frame-uri
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:  # a treia imagine pentru următoarele ANIMATION_TIME frame-uri
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:  # a doua imagine din nou pentru următoarele ANIMATION_TIME frame-uri
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:  # resetează animația după un ciclu complet
            self.img = self.IMGS[0]
            self.img_count = 0

        # Când pasărea cade brusc, nu mai animează bătaia din aripi
        if self.tilt <= -80:  # dacă pasărea este înclinată foarte mult în jos
            self.img = self.IMGS[1]  # folosește imaginea cu aripile la mijloc
            self.img_count = self.ANIMATION_TIME*2  # ajustează contorul pentru a menține această imagine

        # Desenează pasărea cu rotație
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)  # funcție helper pentru a desena imaginea rotită

    def get_mask(self):
        """
        Obține masca pentru detectarea coliziunilor
        :return: Masca pygame pentru imaginea curentă
        """
        return pygame.mask.from_surface(self.img)  # creează o mască din imaginea curentă pentru coliziuni precise


class Pipe():
    """
    Clasa Pipe reprezintă țevile prin care pasărea trebuie să treacă
    """
    GAP = 200  # spațiul dintre țeava de sus și cea de jos
    VEL = 5  # viteza de mișcare a țevilor

    def __init__(self, x):
        """
        Inițializează obiectul țeavă
        :param x: poziția x a țevii (int)
        :return: None
        """
        self.x = x  # poziția x a țevii
        self.height = 0  # înălțimea țevii (va fi setată aleator)

        # poziția țevii de sus și de jos
        self.top = 0  # poziția y a capătului de jos al țevii de sus
        self.bottom = 0  # poziția y a capătului de sus al țevii de jos

        # Pregătește imaginile pentru țevi
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)  # țeava de sus (imaginea întoarsă)
        self.PIPE_BOTTOM = pipe_img  # țeava de jos (imaginea normală)

        self.passed = False  # marchează dacă pasărea a trecut de această țeavă

        self.set_height()  # setează înălțimea aleatoare a țevilor

    def set_height(self):
        """
        Setează înălțimea țevilor în mod aleator
        :return: None
        """
        self.height = random.randrange(50, 450)  # alege o înălțime aleatoare între 50 și 450
        self.top = self.height - self.PIPE_TOP.get_height()  # calculează poziția țevii de sus
        self.bottom = self.height + self.GAP  # calculează poziția țevii de jos

    def move(self):
        """
        Mișcă țeava spre stânga
        :return: None
        """
        self.x -= self.VEL  # deplasează țeava spre stânga cu viteza VEL

    def draw(self, win):
        """
        Desenează ambele țevi (sus și jos)
        :param win: fereastra pygame
        :return: None
        """
        # Desenează țeava de sus
        win.blit(self.PIPE_TOP, (self.x, self.top))  # desenează țeava de sus la poziția calculată
        # Desenează țeava de jos
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))  # desenează țeava de jos la poziția calculată


    def collide(self, bird, win):
        """
        Verifică dacă pasărea se ciocnește cu țeava
        :param bird: obiectul pasăre
        :return: Bool (True dacă există coliziune, False în caz contrar)
        """
        # Obține măștile pentru coliziune
        bird_mask = bird.get_mask()  # masca pasării
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)  # masca țevii de sus
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)  # masca țevii de jos
        
        # Calculează offset-urile pentru verificarea coliziunii
        top_offset = (self.x - bird.x, self.top - round(bird.y))  # offset pentru țeava de sus
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))  # offset pentru țeava de jos

        # Verifică suprapunerea măștilor (coliziunea)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # verifică coliziunea cu țeava de jos
        t_point = bird_mask.overlap(top_mask,top_offset)  # verifică coliziunea cu țeava de sus

        if b_point or t_point:  # dacă există coliziune cu orice țeavă
            return True  # returnează True pentru coliziune

        return False  # nu există coliziune

class Base:
    """
    Clasa Base reprezintă podeaua în mișcare din joc
    """
    VEL = 5  # viteza de mișcare a bazei
    WIDTH = base_img.get_width()  # lățimea imaginii bazei
    IMG = base_img  # imaginea bazei

    def __init__(self, y):
        """
        Inițializează obiectul bază
        :param y: poziția y a bazei (int)
        :return: None
        """
        self.y = y  # poziția y a bazei
        self.x1 = 0  # poziția x a primei imagini a bazei
        self.x2 = self.WIDTH  # poziția x a celei de-a doua imagini a bazei

    def move(self):
        """
        Mișcă baza pentru a crea efectul de derulare
        :return: None
        """
        self.x1 -= self.VEL  # mișcă prima imagine spre stânga
        self.x2 -= self.VEL  # mișcă a doua imagine spre stânga
        
        # Dacă prima imagine iese complet din ecran
        if self.x1 + self.WIDTH < 0:  # verifică dacă imaginea a ieșit complet din ecran
            self.x1 = self.x2 + self.WIDTH  # o readuce după a doua imagine

        # Dacă a doua imagine iese complet din ecran
        if self.x2 + self.WIDTH < 0:  # verifică dacă imaginea a ieșit complet din ecran
            self.x2 = self.x1 + self.WIDTH  # o readuce după prima imagine

    def draw(self, win):
        """
        Desenează baza (două imagini care se mișcă împreună)
        :param win: fereastra pygame
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))  # desenează prima imagine a bazei
        win.blit(self.IMG, (self.x2, self.y))  # desenează a doua imagine a bazei


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotește o imagine și o desenează pe fereastră
    :param surf: suprafața pe care se desenează
    :param image: imaginea de rotit
    :param topLeft: poziția din stânga sus a imaginii
    :param angle: unghiul de rotație (float)
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)  # rotește imaginea
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)  # calculează noul dreptunghi pentru a păstra centrul imaginii

    surf.blit(rotated_image, new_rect.topleft)  # desenează imaginea rotită

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    """
    Desenează fereastra pentru bucla principală a jocului
    :param win: suprafața pygame
    :param birds: lista de păsări
    :param pipes: lista de țevi
    :param score: scorul jocului (int)
    :param gen: generația curentă
    :param pipe_ind: indexul celei mai apropiate țevi
    :return: None
    """
    if gen == 0:  # asigură că generația nu este 0 pentru afișare
        gen = 1
    win.blit(bg_img, (0,0))  # desenează fundalul

    # Desenează toate țevile
    for pipe in pipes:  # pentru fiecare țeavă din lista de țevi
        pipe.draw(win)  # desenează țeava

    # Desenează baza
    base.draw(win)  # desenează baza în mișcare
    
    # Desenează toate păsările
    for bird in birds:  # pentru fiecare pasăre din lista de păsări
        # Desenează liniile de la pasăre la țeavă (pentru vizualizarea rețelei neuronale)
        if DRAW_LINES:  # dacă opțiunea de desenare a liniilor este activată
            try:
                # Desenează o linie de la pasăre la partea de sus a țevii
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                # Desenează o linie de la pasăre la partea de jos a țevii
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass  # ignoră erorile (de exemplu, dacă nu există țevi)
        # Desenează pasărea
        bird.draw(win)  # desenează pasărea

    # Desenează scorul
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))  # creează textul pentru scor
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))  # desenează scorul în colțul din dreapta sus

    # Desenează generația
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))  # creează textul pentru generație
    win.blit(score_label, (10, 10))  # desenează generația în colțul din stânga sus

    # Desenează numărul de păsări în viață
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))  # creează textul pentru numărul de păsări în viață
    win.blit(score_label, (10, 50))  # desenează numărul de păsări în viață sub generație

    pygame.display.update()  # actualizează afișajul


def eval_genomes(genomes, config):
    """
    Execută simularea populației curente de păsări și setează
    fitness-ul lor în funcție de distanța pe care o parcurg în joc.
    """
    global WIN, gen  # folosește variabilele globale
    win = WIN  # fereastra jocului
    gen += 1  # incrementează generația

    # Începe prin crearea listelor care conțin genomul în sine,
    # rețeaua neuronală asociată genomului și obiectul pasăre
    # care folosește acea rețea pentru a juca
    nets = []  # lista pentru rețelele neuronale
    birds = []  # lista pentru păsări
    ge = []  # lista pentru genomuri
    for genome_id, genome in genomes:  # pentru fiecare genom din generația curentă
        genome.fitness = 0  # începe cu un nivel de fitness 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)  # creează rețeaua neuronală din genom
        nets.append(net)  # adaugă rețeaua la listă
        birds.append(Bird(230,350))  # creează o pasăre și o adaugă la listă
        ge.append(genome)  # adaugă genomul la listă

    base = Base(FLOOR)  # creează baza jocului
    pipes = [Pipe(700)]  # creează prima țeavă
    score = 0  # inițializează scorul

    clock = pygame.time.Clock()  # creează un ceas pentru controlul FPS

    run = True  # flag pentru bucla principală
    while run and len(birds) > 0:  # cât timp jocul rulează și există păsări în viață
        clock.tick(30)  # limitează FPS-ul la 30

        for event in pygame.event.get():  # verifică evenimentele pygame
            if event.type == pygame.QUIT:  # dacă utilizatorul închide fereastra
                run = False  # oprește bucla
                pygame.quit()  # închide pygame
                quit()  # închide programul
                break

        pipe_ind = 0  # indexul țevii care este urmărită
        if len(birds) > 0:  # dacă există păsări în viață
            # Determină dacă să folosească prima sau a doua țeavă de pe ecran pentru intrarea în rețeaua neuronală
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1  # folosește a doua țeavă dacă prima a fost depășită

        for x, bird in enumerate(birds):  # dă fiecărei păsări un fitness de 0.1 pentru fiecare frame în care rămâne în viață
            ge[x].fitness += 0.1  # crește fitness-ul genomului
            bird.move()  # mișcă pasărea

            # Trimite poziția păsării, poziția țevii de sus și a celei de jos și determină din rețea dacă să sară sau nu
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # folosim o funcție de activare tanh, deci rezultatul va fi între -1 și 1. Dacă este peste 0.5, sare
                bird.jump()  # face pasărea să sară

        base.move()  # mișcă baza

        rem = []  # lista pentru țevile de eliminat
        add_pipe = False  # flag pentru adăugarea unei noi țevi
        for pipe in pipes:  # pentru fiecare țeavă
            pipe.move()  # mișcă țeava
            # Verifică coliziunea
            for bird in birds:  # pentru fiecare pasăre
                if pipe.collide(bird, win):  # dacă pasărea se ciocnește cu țeava
                    ge[birds.index(bird)].fitness -= 1  # penalizează genomul
                    nets.pop(birds.index(bird))  # elimină rețeaua
                    ge.pop(birds.index(bird))  # elimină genomul
                    birds.pop(birds.index(bird))  # elimină pasărea

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # dacă țeava a ieșit complet din ecran
                rem.append(pipe)  # marchează țeava pentru eliminare

            if not pipe.passed and pipe.x < bird.x:  # dacă pasărea a trecut de țeavă
                pipe.passed = True  # marchează țeava ca fiind depășită
                add_pipe = True  # setează flagul pentru adăugarea unei noi țevi

        if add_pipe:  # dacă trebuie adăugată o nouă țeavă
            score += 1  # crește scorul
            # Poate adăuga această linie pentru a oferi mai multă recompensă pentru trecerea printr-o țeavă (nu este obligatoriu)
            for genome in ge:  # pentru fiecare genom
                genome.fitness += 5  # crește fitness-ul cu 5
            pipes.append(Pipe(WIN_WIDTH))  # adaugă o nouă țeavă

        for r in rem:  # pentru fiecare țeavă de eliminat
            pipes.remove(r)  # elimină țeava din listă

        for bird in birds:  # pentru fiecare pasăre
            # Verifică dacă pasărea a lovit podeaua sau a ieșit în sus din ecran
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))  # elimină rețeaua
                ge.pop(birds.index(bird))  # elimină genomul
                birds.pop(birds.index(bird))  # elimină pasărea

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)  # desenează fereastra jocului

        # Oprește dacă scorul devine suficient de mare
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''


def run(config_file):
    """
    Execută algoritmul NEAT pentru a antrena o rețea neuronală să joace Flappy Bird
    :param config_file: locația fișierului de configurare
    :return: None
    """
    # Încarcă configurația NEAT
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)  # încarcă configurația din fișier

    # Creează populația, care este obiectul de nivel superior pentru o execuție NEAT
    p = neat.Population(config)  # creează populația inițială

    # Adaugă un reporter stdout pentru a arăta progresul în terminal
    p.add_reporter(neat.StdOutReporter(True))  # adaugă reporter pentru terminal
    stats = neat.StatisticsReporter()  # creează un reporter de statistici
    p.add_reporter(stats)  # adaugă reporterul de statistici
    #p.add_reporter(neat.Checkpointer(5))  # adaugă un punct de control (comentat)

    # Rulează pentru maximum 50 de generații
    winner = p.run(eval_genomes, 50)  # execută evaluarea genomurilor pentru 50 de generații

    # Arată statisticile finale
    print('\nBest genome:\n{!s}'.format(winner))  # afișează cel mai bun genom


if __name__ == '__main__':
    # Determină calea către fișierul de configurare. Această manipulare a căii
    # este aici pentru ca scriptul să ruleze cu succes indiferent de
    # directorul de lucru curent.
    local_dir = os.path.dirname(__file__)  # obține directorul curent
    config_path = os.path.join(local_dir, 'config-feedforward.txt')  # construiește calea către fișierul de configurare
    run(config_path)  # execută jocul