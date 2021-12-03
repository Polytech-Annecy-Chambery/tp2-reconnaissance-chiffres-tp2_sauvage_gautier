from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    def binarisation(self, S):
		# creation d'une image vide
        im_bin = Image()
        
        # affectation a l'image im_bin d'un tableau de pixels de meme taille
        # que self dont les intensites, de type uint8 (8bits non signes),
        # sont mises a 0
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))
        
        #boucles imbriquees pour parcourir tous les pixels de l'image
        for l in range(self.H):
            for c in range(self.W):
                # modif des pixels d'intensite >= a S
                if self.pixels[l][c] >= S:
                    im_bin.pixels[l][c] = 255
                else :
                    im_bin.pixels[l][c] = 0
        return im_bin


    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        im_localis = Image()
        #on initialise les variables comme indique dans l'enonce
        l_min = self.H
        c_min = self.W
        l_max = 0
        c_max = 0
        #on parcourt l'image
        for l in range(self.H):
            for c in range(self.W):
                #on regarde si le pixel est noir ou non
                  if self.pixels[l][c] == 0:
                      #on regarde sa position par rapport aux valeurs extremes
                    if l < l_min:
                        l_min = l
                    if c < c_min:
                        c_min = c
                    if l > l_max:
                        l_max = l
                    if c > c_max:
                        c_max =c
                        
        #print("l-min= ",l_min,"  l-max= ",l_max,"  c-min= ",c_min,"  c-max= ",c_max)
        
        im_localis.pixels = self.pixels[l_min:l_max+1,c_min:c_max+1]
        im_localis.H = l_max - l_min
        im_localis.W = c_max - c_min
        
        return (im_localis)


    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        im_resized = Image()
        im_resized.pixels = resize(self.pixels, (new_H,new_W), 0)
        im_resized.pixels = np.uint8(im_resized.pixels*255) #on multiplie par 255 et on met sur 8 bits
        im_resized.H = new_H
        im_resized.W = new_W
        return (im_resized)



    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, im):
        simil = 0
        for l in range(self.H):
            for c in range(self.W):
                if (self.pixels[l][c] == im.pixels[l][c]):
                    simil = simil + 1
        return (simil/(self.H*self.W))

