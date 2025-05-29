import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

class ThermalImageProcessor:
    def __init__(self):
        self.color_map = {
            'hot': cv2.COLORMAP_JET,
            'rainbow': cv2.COLORMAP_RAINBOW,
            'ocean': cv2.COLORMAP_OCEAN,
            'thermal': cv2.COLORMAP_INFERNO
        }
        
    def process_image(self, image_path, colormap='thermal', save_path=None):
        """
        Process an image to create a thermal-like visualization
        """
        try:
            # Read and validate the image
            if not os.path.exists(image_path):
                raise ValueError("Image file does not exist")
            
            # Read the image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read the image")

            # Convert BGR to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Convert to grayscale
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

            # Apply histogram equalization to enhance contrast
            equalized = cv2.equalizeHist(gray)

            # Apply some noise reduction
            denoised = cv2.medianBlur(equalized, 5)

            # Create thermal visualization
            selected_map = self.color_map.get(colormap, cv2.COLORMAP_INFERNO)
            thermal = cv2.applyColorMap(denoised, selected_map)

            # Convert thermal to RGB for consistent color space
            thermal_rgb = cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)

            # Save if path is provided
            if save_path:
                cv2.imwrite(save_path, cv2.cvtColor(thermal_rgb, cv2.COLOR_RGB2BGR))

            # Analyze the thermal image
            moisture_analysis = self.analyze_thermal_image(thermal_rgb)
            
            return {
                'thermal_image': thermal_rgb,
                'moisture_levels': moisture_analysis['moisture_levels'],
                'recommendations': moisture_analysis['recommendations']
            }

        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def analyze_thermal_image(self, thermal_rgb):
        """
        Analyze the thermal image and return moisture levels and recommendations
        """
        try:
            # Ensure we have a numpy array
            if not isinstance(thermal_rgb, np.ndarray):
                raise ValueError("Invalid image format")

            # Convert to HSV for analysis
            hsv = cv2.cvtColor(thermal_rgb, cv2.COLOR_RGB2HSV)

            # Define moisture zones based on color ranges
            zones = {
                'high_moisture': ([100, 50, 50], [140, 255, 255]),    # Blue range
                'medium_moisture': ([40, 50, 50], [80, 255, 255]),    # Green range
                'low_moisture': ([0, 50, 50], [30, 255, 255])         # Red/Yellow range
            }

            # Calculate moisture levels
            moisture_levels = {}
            total_pixels = thermal_rgb.shape[0] * thermal_rgb.shape[1]

            for zone, (lower, upper) in zones.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                zone_pixels = np.sum(mask > 0)
                percentage = (zone_pixels / total_pixels) * 100
                moisture_levels[zone] = round(percentage, 2)

            # Generate recommendations based on moisture levels
            recommendations = self.generate_recommendations(moisture_levels)

            return {
                'moisture_levels': moisture_levels,
                'recommendations': recommendations
            }

        except Exception as e:
            raise Exception(f"Error in thermal analysis: {str(e)}")

    def generate_recommendations(self, moisture_levels):
        """
        Generate irrigation recommendations based on moisture analysis
        """
        try:
            low_moisture = moisture_levels.get('low_moisture', 0)
            medium_moisture = moisture_levels.get('medium_moisture', 0)
            high_moisture = moisture_levels.get('high_moisture', 0)

            if low_moisture > 40:
                return [{
                    'priority': 'High',
                    'action': 'Immediate irrigation required',
                    'details': f'Large dry areas detected ({low_moisture:.1f}% of field). Schedule irrigation within 24 hours.'
                }]
            elif medium_moisture > 50:
                return [{
                    'priority': 'Medium',
                    'action': 'Monitor moisture levels',
                    'details': f'Adequate moisture present ({medium_moisture:.1f}% of field). Plan irrigation in 2-3 days.'
                }]
            elif high_moisture > 30:
                return [{
                    'priority': 'Low',
                    'action': 'No immediate action required',
                    'details': f'Good moisture levels detected ({high_moisture:.1f}% of field). Continue monitoring.'
                }]
            else:
                return [{
                    'priority': 'Medium',
                    'action': 'Assessment needed',
                    'details': 'Unclear moisture distribution. Physical inspection recommended.'
                }]

        except Exception as e:
            raise Exception(f"Error generating recommendations: {str(e)}")

    def enhance_thermal_image(self, thermal_rgb):
        """
        Enhance the thermal image for better visualization
        """
        try:
            # Convert to HSV for color manipulation
            hsv = cv2.cvtColor(thermal_rgb, cv2.COLOR_RGB2HSV)

            # Enhance saturation
            hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)
            
            # Enhance value (brightness)
            hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.1)

            # Convert back to RGB
            enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

            # Apply slight sharpening
            kernel = np.array([[-1,-1,-1],
                             [-1, 9,-1],
                             [-1,-1,-1]]) / 9
            enhanced = cv2.filter2D(enhanced, -1, kernel)

            return enhanced

        except Exception as e:
            raise Exception(f"Error enhancing thermal image: {str(e)}")