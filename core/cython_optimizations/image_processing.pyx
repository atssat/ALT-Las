import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def process_image(np.ndarray[np.uint8_t, ndim=3] image):
    cdef int height = image.shape[0]
    cdef int width = image.shape[1]
    cdef int channels = image.shape[2]
    cdef np.ndarray[np.uint8_t, ndim=3] result = np.zeros_like(image)
    
    # Fast image processing implementation
    for i in range(height):
        for j in range(width):
            for k in range(channels):
                result[i, j, k] = 255 - image[i, j, k]
    
    return result