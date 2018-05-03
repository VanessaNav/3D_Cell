from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QPointF, Qt, QLineF
from PyQt5.QtGui import QPen, QBrush, QPixmap, QImage

class ImageView(QGraphicsView):
    '''
    Esta clase carga una imagen y la información de curvas y puntos. También devuelve las líneas y puntos.
    NOTA: Los métodos para escribir curvas y puntos los consideraremos en el proyecto.
    '''
    def __init__(self):
        super().__init__()

        # Secciones (coordenadas de los puntos)
        self.sections = []
        # Partículas
        self.particles = []
        # Curvas (dibujos)
        self.curves = []

        # Imagen
        self.imageName = None
        self.image = None
        self.imagePixMap = None

        # Escena que debemos añadir al plano de dibujo
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Colores para el dibujo de curvas y puntos
        self.curveColor = Qt.cyan  #QColor.fromRgb(255, 105, 180)
        self.pointColor = Qt.blue

        # Objetos para el dibujo de curvas
        self.cPen = QPen(self.curveColor)            # Se crea un objeto pen
        self.cPen.setWidth(5)
        self.cBrush = QBrush(Qt.SolidPattern)        # Se crea un objeto brush (quizá algo de transparencia estaría bien.
        self.cBrush.setColor(self.curveColor)
        self.cPen.setBrush(self.cBrush)

        # Objetos para el dibujo de puntos
        self.pPen = QPen(self.pointColor)            # Se crea un objeto pen
        self.pPen.setWidth(1)
        self.pBrush = QBrush(Qt.SolidPattern)        # Se crea un objeto brush (quizá algo de transparencia estaría bien.
        self.pBrush.setColor(self.pointColor)
        self.pPen.setBrush(self.pBrush)

        # Estructuras de datos auxiliares: Curva/punto actual
        self.currentCurveStart = None
        self.currentCurveEnd = None
        self.currentCurvePoints = None
        self.currentCurveMarks = None
        self.lastPoint = None

    def loadImage(self, imageFileName):
        self.imageName = imageFileName
        self.image = QImage(imageFileName)
        self.imagePixMap = QPixmap().fromImage(self.image)
        self.scene.addPixmap(self.imagePixMap)
        self.scene.update()
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        # Debe cargar también las curvas y los puntos aquí.

    def drawPoint(self, point):
        # Añade el punto y actualiza
        self.currentCurveMarks.append(self.scene.addEllipse(point.x(), point.y(), 1, 1, self.cPen, self.cBrush))
        self.scene.update()

    def drawLine(self, startPoint, endPoint):
        # Dibuja la línea
        self.currentCurveMarks.append(self.scene.addLine(QLineF(startPoint, endPoint), self.cPen))

    def drawParticle(self, point):
        # Añade la partícula
        self.scene.addEllipse(point.x(), point.y(), 15, 15, self.pPen, self.pBrush)
        self.scene.update()

    def mousePressEvent(self, event):
        # Crea el punto
        point = QPointF(self.mapToScene(event.pos()))
        # Almacena la referencia
        self.currentCurveStart = point
        self.lastPoint = point
        # Inicializa la curva
        self.currentCurveMarks = []
        self.currentCurvePoints = []


    def mouseMoveEvent(self, event):
        # Crea un punto en la posición marcada por el ratón
        point = QPointF(self.mapToScene(event.pos()))
        # Dibuja el punto de la curva/partícula
        self.drawPoint(point)
        self.drawLine(point, self.lastPoint)
        # Lo añade a la curva actual y guarda la referencia
        self.currentCurvePoints.append(point)
        self.lastPoint = point

    def mouseReleaseEvent(self, event):
        # Si se trata de un punto, lo dibuja.
        if self.currentCurveMarks is None or len(self.currentCurveMarks)<10:
            # Borra la curva primero
            for mark in self.currentCurveMarks:
                self.scene.removeItem(mark)
            # Dibuja la partícula
            self.drawParticle(self.currentCurveStart)
            # La añade
            self.particles.append((self.currentCurveStart.x(), self.currentCurveStart.y()))

        else:
            # Cierra la curva
            self.currentCurveEnd = QPointF(self.mapToScene(event.pos()))
            self.currentCurvePoints.append(self.currentCurveEnd)
            self.drawPoint(self.currentCurveEnd)
            # Une el punto del principio y del final.
            self.drawLine(self.currentCurveStart, self.currentCurveEnd)
            # Guarda los datos de la curva
            self.curves.append(self.currentCurveMarks)
            self.sections.append(list(map(lambda point: (point.x(), point.y()), self.currentCurvePoints)))


    def removeLastCurve(self):
        if len(self.sections)==0:
            return
        # Borra la curva primero
        for mark in self.curves.pop():
            self.scene.removeItem(mark)
        # Borra los datos de la sección
        self.sections.pop()


    def clear(self):
        # Borra las marcas
        from itertools import chain
        for mark in chain(*self.curves):
            self.scene.removeItem(mark)
        # Borra partículas y secciones (coordenadas)
        self.sections = []
        self.particles = []


    ### Quedarían por implementar SOLAMENTE estas funciones
    #loadSections, que se le pasa un fichero con las curvas y las carga en self.sections y las dibuja.
    #loadParticules, que toma un fichero y carga las particulas.

    #La escritura la haremos en project.

    def loadSections(self, sectionFileName):
        '''
        Carga los curvas (coordenadas)
        '''
        pass

    def loadParticles(self, particlesFileName):
        '''
        Carga los puntos
        '''
        pass