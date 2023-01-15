import numpy as np

from skimage import io
from skimage.color import rgb2gray
from skimage.util import invert
from skimage.transform import rescale
from skimage.filters import sobel, sobel_v, sobel_h
from skimage.draw import polygon


class SeamCarver:
    def __init__(self, image_file_name: str, scale_ratio=1) -> None:
        self.image_file_name = image_file_name
        self.img = rescale(io.imread(self.image_file_name), scale_ratio, channel_axis=2)
        self.directions = self.get_directions(self.get_sobel_edges())
    
    def get_image_shape(self):
        return self.img.shape[0], self.img.shape[1]
    
    def get_sobel_edges(self):
        return sobel(rgb2gray(self.img))

    def get_energies_and_directions(self, sobel_edges):
        row_number, col_number = sobel_edges.shape
        energy = np.zeros((row_number, col_number))
        energy[-1,:] = sobel_edges[-1,:]

        directions = np.zeros((row_number, col_number), dtype=int)

        for row_id in range(row_number-2, -1, -1):
            for col_id in range(col_number):
                previous_row_id = row_id + 1
                current_pixel = sobel_edges[row_id, col_id]

                if col_id == 0:
                    down = energy[previous_row_id, 0]
                    right = energy[previous_row_id, 1]
                    direction = np.argmin([down, right])
                elif col_id == col_number-1:
                    down = energy[previous_row_id, col_id]
                    left = energy[previous_row_id, col_id-1]
                    direction = np.argmin([left, down])-1
                else:
                    left = energy[previous_row_id, col_id-1]
                    down = energy[previous_row_id, col_id]
                    right = energy[previous_row_id, col_id+1]
                    direction = np.argmin([left, down, right])-1

                directions[row_id,col_id] = direction
                energy[row_id,col_id] = current_pixel + energy[previous_row_id, col_id+direction]

        return energy, directions
    
    def get_directions(self, image):
        row_number, col_number = image.shape
        energy = np.zeros(col_number)
        p_energy = image[-1,:].copy()

        directions = np.zeros((row_number, col_number), dtype=int)

        for row_id in range(row_number-2, -1, -1):
            for col_id in range(col_number):
                if col_id == 0:
                    direction = np.argmin(p_energy[col_id:col_id+2])
                elif col_id == col_number-1:
                    direction = np.argmin(p_energy[col_id-1:col_id+1])-1
                else:
                    direction = np.argmin(p_energy[col_id-1:col_id+2])-1

                directions[row_id, col_id] = direction

                energy[col_id] = image[row_id, col_id] + p_energy[col_id+direction]
            p_energy = energy.copy()

        return directions
    
    def get_seam_start_of_lowest_energy(self, energies):
        # return np.argmin(energies[0, :])
        return np.argmin(energies)

    def get_seam(self, directions, seam_at=0):
        row_number, col_number = directions.shape
        seam = np.zeros((row_number,2), dtype=int)

        seam[0] = [0, seam_at]
        for row_id in range(1,row_number):
            # print(f"s: {seam_at} d{directions[row_id-1, seam_at]}")
            seam_at = seam_at + directions[row_id-2, seam_at]
            seam[row_id] = [row_id, seam_at]

        return seam
    
    def remove_seam_from_image(self, image, seam):
        if len(image.shape) == 3:
            row, col, channels = image.shape
            result = np.zeros((row, col-1, channels), dtype=image.dtype)
        else:
            row, col = image.shape
            result = np.zeros((row, col-1), dtype=image.dtype)

        for i in range(row):
            seam_at = seam[i, 1]
            result[i] = np.r_[image[i, :seam_at], image[i, seam_at+1:]]

        return result
    
    def shrink_image_best(self, number_of_pixels):
        img_rgb = self.img.copy()
        edges = self.get_sobel_edges()
        for _ in range(number_of_pixels):
            energies, directions = self.get_energies_and_directions(edges)
            seam = self.get_seam(directions, self.get_seam_start_of_lowest_energy(energies[0, :]))
            img_rgb = self.remove_seam_from_image(img_rgb, seam)
            edges = self.remove_seam_from_image(edges, seam)
        return img_rgb
    
    def shrink_image_medium(self, number_of_pixels):
        img_rgb = self.img.copy()
        edges = self.get_sobel_edges()
        energies, directions = self.get_energies_and_directions(edges)
        energies_first_row = energies[0, :]
        for _ in range(number_of_pixels):
            directions = self.get_directions(edges)
            seam_at = self.get_seam_start_of_lowest_energy(energies_first_row)
            np.delete(energies_first_row, seam_at)
            seam = self.get_seam(directions, seam_at)
            img_rgb = self.remove_seam_from_image(img_rgb, seam)
            edges = self.remove_seam_from_image(edges, seam)
        return img_rgb
    
    def shrink_image_worst(self, number_of_pixels):
        img_rgb = self.img.copy()
        edges = self.get_sobel_edges()
        energies, directions = self.get_energies_and_directions(edges)
        energies_first_row = energies[0, :]
        for _ in range(number_of_pixels):
            seam_at = self.get_seam_start_of_lowest_energy(energies_first_row)
            np.delete(energies_first_row, seam_at)
            seam = self.get_seam(directions, seam_at)
            img_rgb = self.remove_seam_from_image(img_rgb, seam)
            directions = self.remove_seam_from_image(directions, seam)
        return img_rgb

    def draw_seam(self, seam_at, image=None, draw_mode=None):
        if image is None:
            image = self.img.copy()
        
        if draw_mode is None:
            return image
        elif draw_mode == "column":
            image[:, seam_at, :] = 0
            return image
        elif draw_mode == "seam":
            seam = self.get_seam(self.directions, seam_at)
            for r in seam:
                image[r[0], r[1], :] = [1, 0, 0]
            return image
