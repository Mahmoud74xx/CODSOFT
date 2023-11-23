import cv2
from cv2 import CascadeClassifier, rectangle
import tkinter as tk
from tkinter import filedialog


# function to open a file dialog and get the path to the image file
def get_image_path():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("JPEG", "*.jpg"), ("JPEG", "*.jpeg"), ("All files", "*.*")]
    )
    return file_path

# function to detect faces and display the image
def detect_faces():
    global original_image_tk, detected_image_tk  # Add global variables
    image_path = get_image_path()
    if image_path:
        # Load the image
        image = cv2.imread(image_path)
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces using the Haar cascade classifier
        classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
        bboxes = classifier.detectMultiScale(gray_image)
        # Draw rectangles around the faces
        for box in bboxes:
            x, y, width, height = box
            x2, y2 = x + width, y + height
            rectangle(image, (x, y), (x2, y2), (0,0,255), 4)
        # Resize images to fixed size
        original_image = cv2.resize(cv2.imread(image_path, cv2.IMREAD_UNCHANGED), (600, 500))
        detected_image = cv2.resize(image, (600, 500))
        original_image_tk = tk.PhotoImage(data=cv2.imencode('.png', original_image)[1].tobytes())  # Assign to global variable
        detected_image_tk = tk.PhotoImage(data=cv2.imencode('.png', detected_image)[1].tobytes())  # Assign to global variable
        images = tk.Frame(root)
        images.grid(row=0, column=0, columnspan=2)
        tk.Label(images, image=original_image_tk).pack(side="left", padx=10, pady=10)
        tk.Label(images, image=detected_image_tk).pack(side="right", padx=10, pady=10)
        # Display number of faces detected
        num_faces = len(bboxes)
        label_num_faces.config(text=f"Number of Faces Detected: {num_faces}")


# Create a function to clear the image display
def clear_image_display():
    global original_image_tk, detected_image_tk  # Add global variables
    cv2.destroyAllWindows()
    label_num_faces.config(text="")
    # Reset global variables to None
    original_image_tk = None
    detected_image_tk = None

# Create the GUI
root = tk.Tk()
root.title("Face Detection")
# Create a button to detect faces
button_detect_faces = tk.Button(root, text="Detect Faces", command=detect_faces)
button_detect_faces.grid(row=1, column=0, padx=10, pady=10)
# Create a button to clear the image display
button_clear_display = tk.Button(root, text="Clear Display", command=clear_image_display)
button_clear_display.grid(row=1, column=1, padx=10, pady=10)
# Create a label for the number of faces detected
label_num_faces = tk.Label(root, text="")
label_num_faces.grid(row=2, column=0, columnspan=2)
# Start the GUI event loop
root.mainloop()
