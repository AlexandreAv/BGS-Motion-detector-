import numpy as np
import cv2
from threading import Thread, RLock
import pdb


lock = RLock()


def background_subtraction(path='0'):
    cap = cv2.VideoCapture(path)  # On récupère la flux vidéo
    is_there_movement = IsThereMovement()

    if cap.isOpened():  # On vérifie si le flux vidéo a été ouvert correctement
        print('la vidéo a pu être ouverte')

        while True:  # On ouvre une boucle pour lire le flux
            _, frame_current = cap.read()  # On lit l'image actuelle
            _, frame_next = cap.read()  # On lit l'image suivante

            if frame_next is None:  # On regarde si la vidéo n'arrive pas à la fin
                break  # Si c'est le cas on coupe le boucle

            frame_current = cv2.cvtColor(frame_current, cv2.COLOR_BGR2GRAY)
            frame_next = cv2.cvtColor(frame_next, cv2.COLOR_BGR2GRAY)  # On procède à une mise en grayscale des images

            sub_frame = cv2.subtract(frame_next, frame_current)  # On soustraie les images

            with lock:
                thresh = cv2.adaptiveThreshold(sub_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            # pdb.set_trace()

            cv2.imshow('frame', thresh)  # On affiche le résultat

            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

    else:
        print("la vidéo n'a pas pu être ouverte")


class IsThereMovement(Thread):
    def __init__(self, limit_image):
        Thread.__init__(self)
        self.images = []
        self.limit_image = limit_image

    def run(self, image, percentage_validity):
        return self.is_there_movement(image, percentage_validity)

    def add_image(self, image):
        self.images.append(image)

        if len(self.images > self.limit_image):
            self.run()

    @staticmethod
    def is_there_movement(image, percentage_validity):
        width, height = image.shape
        pixel_changed = 0

        for x in image:
            for y in x:
                if y == 1:
                    pixel_changed += 1

        if pixel_changed > (width * height) * (percentage_validity / 100):
            return True
        else:
            return False


background_subtraction(r"D:\Users\Alexandre\Documents\Programation\Projets\Python\Motion Detector\vidéo.mp4")
