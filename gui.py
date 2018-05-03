import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QPushButton, \
     QAction, QMenuBar, QFileDialog, QCheckBox, QHBoxLayout, \
     QDesktopWidget, QWidget, QMainWindow, QLineEdit

from project import Project
from imageview import ImageView
import utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Proyecto
        self.project = None

        # Título
        self.setWindowTitle("3D Cell Reconstruction")

        # Inicializa el menú
        self.initMenubar()

        # Visor de las imágenes (imagen y control van en el mismo layout)
        # NOTA: Es el objeto central del objeto QMainWindow, que tiene eso, una barra de estado, etc. Podemos volver al QWidget si es fuese mejor.
        self.imageViewer = QWidget(self)
        self.imageViewer.setLayout(QGridLayout())
        # Fija márgenes para centrar la imagen
        self.imageViewer.layout().setColumnStretch(0, 0)
        self.imageViewer.layout().setColumnStretch(2, 0)
        self.imageViewer.layout().setRowStretch(1, 0)
        self.imageViewer.layout().setRowStretch(3, 0)
        # Crea un campo de texto para mostrar el nombre de la imagen
        self.imageName = QLineEdit("No project loaded")
        self.imageName.setReadOnly(True)
        self.imageViewer.layout().addWidget(self.imageName, 0,1)
        # Crea un objeto de la clase ImageView para mostrar la imagen y dibujar
        self.imageView = ImageView()
        self.imageViewer.layout().addWidget(self.imageView, 2, 1)
        # Inicializa los botones de control
        self.initControlLayout()
        self.imageViewer.layout().addLayout(self.control_layout, 3, 0, 1, 3)
        # Lo situa como objeto pricipal de la aplicación.
        self.setCentralWidget(self.imageViewer)

        # NOTA: Como inicialmente no hay proyecto abierto, deshabilita los botones.
        self.enableControls(False)

    def initMenubar(self):
        '''
        Crea el menú de la aplicación y lo almacena en self.menuBar
        '''
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)
        self.menuBar.setNativeMenuBar(False)  # Necesario para que funcione en MacOS

        # Menu File
        fileMenu = self.menuBar.addMenu("File")
        openAction = QAction('Open image sequence', self)
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)
        exitAction = QAction('Exit', self)
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.close)

        # Menu Display
        displayMenu = self.menuBar.addMenu("Display")
        gen3DAction = QAction('Generate 3D structure', self)
        displayMenu.addAction(gen3DAction)
        gen3DAction.triggered.connect(self.gen3D)

        # Help Display
        helpMenu = self.menuBar.addMenu("Help")
        aboutAction = QAction("About", self)
        helpMenu.addAction(aboutAction)
        # aboutAction.triggered.connect(self.about)  # Una ventana que muestre tu nombre, y eso.


    def initControlLayout(self):
        '''
        Añade los botones para navegar sobre las imágenes en un imgViewerLayout
        denominado self.control_layout.
        '''

        # Alante y atrás
        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon('resources/next.png'))
        self.btn_next.setFixedWidth(50)
        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(QIcon('resources/back.png'))
        self.btn_prev.setFixedWidth(50)

        # Borrar y deshacer
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setFixedWidth(80)
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.setFixedWidth(80)

        # Mostrar o no información de las imágenes anteriores.
        self.check_showC = QCheckBox("Previous Image Curves")
        self.check_showP = QCheckBox("Previous Image Particles")
        self.check_showC.setChecked(False)
        self.check_showP.setChecked(False)

        # Panel para colocar los controles.
        self.control_layout = QHBoxLayout()

        # Coloca los controles en el imgViewerLayout
        self.control_layout.addWidget(self.btn_prev)
        self.control_layout.addWidget(self.btn_next)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.check_showC)
        self.control_layout.addWidget(self.check_showP)
        self.control_layout.addWidget(self.btn_undo)
        self.control_layout.addWidget(self.btn_clear)

        # Conecta los componentes con las acciones correspondientes.
        self.btn_next.clicked.connect(self.next)
        self.btn_prev.clicked.connect(self.prev)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_undo.clicked.connect(self.undo)
        #self.check_showC.clicked.connect(self.showC)
        #self.check_showP.clicked.connect(self.showP)


    def enableControls(self, state):
        '''
            Habilita o deshabilita los controles y la vista de la imagen.
        '''
        self.imageName.setEnabled(state)
        self.imageView.setEnabled(state)
        self.btn_next.setEnabled(state)
        self.btn_prev.setEnabled(state)
        self.btn_clear.setEnabled(state)
        self.btn_undo.setEnabled(state)
        self.check_showC.setEnabled(state)
        self.check_showP.setEnabled(state)


    def updateWindowSize(self):
        '''
            Aujsta el tamaño de la ventana y la centra
        '''
        # Calcula el tamaño ideal para la vista y la ventana. Para ello determina, el ratio
        # en función la máxima altura o anchura que puede tener la imagen.
        if not self.project is None:
            ratioWidth = (screenSize.getCoords()[2] - 100) / (self.project.imgShape[1])
            ratioHeight = (screenSize.getCoords()[3] - 150) / (self.project.imgShape[0])
            ratio = ratioWidth if ratioWidth < ratioHeight else ratioHeight
            self.imageView.setFixedWidth(int(self.project.imgShape[1] * ratio))
            self.imageView.setFixedHeight(int(self.project.imgShape[0] * ratio))
            # Ajusta el tamaño de la ventana.
            self.adjustSize()

        # Centra la ventana
        windowPosition = self.geometry()
        windowPosition.moveCenter(screenSize.center())
        self.move(windowPosition.topLeft())


    def updateImageView(self):
        '''
            Actualiza la imagen
        '''
        # Actualiza el texto y la imagen (recortada).
        self.imageName.setText(self.project.imgSequence[self.project.currentImgId])
        utils.cropImageBorders(self.project.folder + '/' + self.project.imgSequence[self.project.currentImgId])
        self.imageView.loadImage(self.project.folder + '/' + self.project.imgSequence[self.project.currentImgId])


    def open(self):
        '''
        Abre un proyecto.
        '''
        # Selecciona un directorio de trabajo para cargarlo en un proyecto.
        selectedDirectory = str(QFileDialog.getExistingDirectory(self, "Select directory"))

        # Vuelve si se ha cancelado la apertura.
        if len(selectedDirectory)==0:
            # NOTA: Fíjate que lo que hacemos es dejarlo como estaba. Si había cargado un proyecto, se queda
            #       abierto y los botones y eso habilitados. Si no había nada abierto, sigue sin abrirse.
            return

        # NOTA: Solamente llega aquí si se ha seleccionado un directorio.
        # Se crea el proyecto
        self.project = Project(selectedDirectory)

        # Si en la carpeta seleccionada no hay ninguna imagen, deshabilitamos
        if len(self.project.imgSequence) == 0:
            #self.imageView.scene.clear()
            self.enableControls(False)
            return

        # NOTA: Solamente llega aquí si el proyecto tiene imágenes

        # Actualiza el tamaño de la ventana.
        self.updateWindowSize()

        # Muestra la información actual del proyecto.
        self.updateImageView()

        # Habilita los controles.
        self.enableControls(True)

    def next(self):
        '''
        Pasa a la siguiente imagen.
        '''
        self.project.next()
        self.updateImageView()

    def prev(self):
        '''
        Pasa a la imagen anterior.
        '''
        self.project.prev()
        self.updateImageView()

    def undo(self):
        self.imageView.removeLastCurve()

    def clear(self):
        self.imageView.clear()


    def gen3D(self):
        '''
        Genera la reconstrucción 3D
        '''
        pass

app = QApplication(sys.argv)
screenSize = QDesktopWidget().availableGeometry()
mainWindow = MainWindow()
mainWindow.show()
mainWindow.updateWindowSize()
app.exec_()

