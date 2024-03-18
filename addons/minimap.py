from qtpy.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QGridLayout, QComboBox, QMenu
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QAction
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import napari

class MiniMap(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.title = QLabel('Mini Map')

        self.label_well_plate = QLabel('Choose Wellplate')
        self.box_well_plate = QComboBox()
        well_plate_list = ['6-Well','12-Well','24-Well']
        self.box_well_plate.addItems(well_plate_list)


        self.button = QPushButton('Minimap')
        self.button.clicked.connect(self.add_minimap)

        self.checkpoint = QPushButton('Checkpoint')
        self.checkpoint.clicked.connect(self.add_checkpoint)
        self.checkpoint_num = 1

        self.cp_edit = QLineEdit()
        self.cp_edit.setPlaceholderText('Description of Checkpoint')

        self.clear_checkpoint = QPushButton('Clear Checkpoints')
        self.clear_checkpoint.clicked.connect(self.clear)

        self.box_checkpoints = QComboBox()

        self.description = QTextEdit()
    
        

        self.edit_x = QLineEdit('')
        self.edit_x.setPlaceholderText('X')
        self.edit_y = QLineEdit('')
        self.edit_y.setPlaceholderText('Y')
        self.edit_x.textChanged.connect(self.update_map)
        self.edit_y.textChanged.connect(self.update_map)

        

        self.layout.addWidget(self.title,0,0,1,2)
        self.layout.addWidget(self.button,1,0,1,2)
        self.layout.addWidget(self.label_well_plate,2,0,1,1)
        self.layout.addWidget(self.box_well_plate,2,1,1,1)
        self.layout.addWidget(self.edit_x,3,0,1,1)
        self.layout.addWidget(self.edit_y,3,1,1,1)
        self.layout.addWidget(self.cp_edit,4,0,1,1)
        self.layout.addWidget(self.checkpoint,4,1,1,1)
        self.layout.addWidget(self.box_checkpoints,5,0,1,1)
        self.layout.addWidget(self.clear_checkpoint,5,1,1,1)
        self.layout.addWidget(self.description,8,0,1,2)


        self.setLayout(self.layout)

        self.figure = None  # Initialize figure variable
        self.scatter = None  # Initialize scatter variable
        self.checkpoints = None
        self.checkpoint_data_list = []

    def add_minimap(self):
        image_path = 'images/6-wellplate_new.png'
        img = Image.open(image_path)
        x_min, x_max = -1280, 1280
        y_min, y_max = -850, 850

        if self.figure is not None:
            # Clear the previous figure to avoid duplicate plotting
            self.ax.clear()
        else:
            # Create a new figure if it doesn't exist
            self.figure, self.ax = plt.subplots()
            self.canvas = FigureCanvas(self.figure)
            self.layout.addWidget(self.canvas, 6, 0, 1, 2)
            self.setLayout(self.layout)

        self.ax.imshow(np.array(img), extent=[x_min, x_max, y_min, y_max], aspect=(1200/1280))
        self.canvas.draw()

    def update_map(self):
        y = float(self.edit_y.text())
        x = float(self.edit_x.text())

        print(y)

        red_point_coordinates = (x, y)

        if self.scatter is not None:
            # If scatter exists, update its data
            self.scatter.set_offsets([red_point_coordinates])
        else:
            # If scatter doesn't exist, create it
            self.scatter = self.ax.scatter(*red_point_coordinates, color='red', marker='o')

        # Draw the updated figure
        self.canvas.draw()
        

    def add_checkpoint(self):
        y = float(self.edit_y.text())
        x = float(self.edit_x.text())
        cp_coordinates = (x, y)
        cp_label = len(self.checkpoint_data_list) + 1  # Use the length of the list to determine the label
        
        self.checkpoints = self.ax.scatter(*cp_coordinates, color='magenta',marker ='o')
        
        self.ax.text(*cp_coordinates, cp_label, color='black', ha='center', va='center')
        self.canvas.draw()

        checkpoint_data = {'marker': self.checkpoints, 'label': cp_label}

        self.checkpoint_data_list.append(checkpoint_data)

        self.box_checkpoints.addItem(str(cp_label))

        description = self.cp_edit.text()
        self.description.insertPlainText(f'{cp_label}: {description} \n')

        self.cp_edit.clear()

    def clear(self):
        cp_label = self.box_checkpoints.currentText()

        for checkpoint_data in self.checkpoint_data_list:
            if str(checkpoint_data['label']) == cp_label:
                # Remove the marker and label
                checkpoint_data['marker'].remove()

                # Update the canvas to reflect the changes
                self.canvas.draw()

                # Remove the checkpoint data from the list
                self.checkpoint_data_list.remove(checkpoint_data)

                # Remove the label from the GUI element
                item_index = self.box_checkpoints.findText(str(cp_label))
                self.box_checkpoints.removeItem(item_index)

                break

        # Update the labels of all remaining checkpoints
        for i, checkpoint_data in enumerate(self.checkpoint_data_list, start=1):
            checkpoint_data['label'] = i
            self.box_checkpoints.setItemText(i - 1, str(i))  # Update the text in the combo box

        self.update_map()
