import fnmatch
import os
#import imageio
import cv2
import utils

class Project():
    def __init__(self, folder):
        self.folder = folder                                                 # carpeta del proyecto
        self.imgSequence = fnmatch.filter(os.listdir(self.folder), '*.jpg')  # nombres de las imágenes de la secuencia

        # NOTA: Si no hay imágenes, tiene que volver.
        if not self.imgSequence:
            print("There is no images in this folder")
            return

        # Si hay imágenes, crea la carpeta donde se guardarán los datos.
        if not os.path.exists(self.folder + "/data/"):
            os.makedirs(self.folder + "/data/")

        # Se coloca en la primera imagen
        self.currentImgId = 0
        #y recorta sus bordes negros
        utils.cropImageBorders(self.folder + '/' + self.imgSequence[self.currentImgId])

        # Tamaño. Asume que todas las imágenes iguales.
        #self.imgShape = imageio.imread(self.folder + '/' + self.imgSequence[self.currentImgId]).shape
        self.imgShape = cv2.imread(self.folder + '/' + self.imgSequence[self.currentImgId]).shape

        # Crea las estructuras de datos para el trabajo.
        # self.imgCurves = dict()     # diccionario para guardar cada curva de la imagen como clave, y como valores su lista de puntos
        # self.imgParticles = dict()  # diccionario para guardar cada partícula de la imagen como clave, y como valores su lista de puntos
        # self.curveCounter = 1       # contador para indicar la curva
        # self.particleCounter = 1    # contador de partículas
        # self.pointList = []         # lista de puntos para las curvas de la imagen
        # self.particleList = []      # lista de particulas
        # self.globalList = []        # lista para llevar ordenados los ids de curvas y partículas que se van dibujando en las imgs (para el UNDO)


    def next(self):
        if self.currentImgId<len(self.imgSequence)-1:
            self.currentImgId+=1

    def prev(self):
        if self.currentImgId>0:
            self.currentImgId -= 1