import cv2
import numpy as np
from scipy.fftpack import fftshift, ifftshift, fft2, ifft2

def optical_to_sar(optical_image):
  # Convert the optical image to grayscale
  optical_image = cv2.cvtColor(optical_image, cv2.COLOR_BGR2GRAY)

  # Apply Fourier transform to the optical image
  optical_fft = fftshift(fft2(optical_image))

  # Apply some processing here to convert the optical FFT to SAR FFT
  # This is a complex process that depends on the specific characteristics of your SAR system
  # For the sake of this example, we'll just use the optical FFT as the SAR FFT
  sar_fft = optical_fft

  # Apply inverse Fourier transform to get the SAR image
  sar_image = np.abs(ifft2(ifftshift(sar_fft)))

  # Normalize the SAR image to [0, 1]
  sar_image = (sar_image - sar_image.min()) / (sar_image.max() - sar_image.min())

  return sar_image

# Load the optical image
optical_image = cv2.imread("C:\\Users\\Lenovo\\Desktop\\SAR\\week3\\assets\\nuaa.jpg")

# Convert the optical image to SAR
sar_image = optical_to_sar(optical_image)

# write the SAR image to disk
cv2.imwrite("C:\\Users\\Lenovo\\Desktop\\SAR\\week3\\assets\\nuaa_sar.jpg", sar_image * 255)

# Display the SAR image
#cv2.imshow('SAR Image', sar_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()