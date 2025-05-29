# ⭐AgriVision - Comprehensive Agricultural Management System

AgriVision is a comprehensive agricultural management platform designed to assist farmers with multiple aspects of crop management.  
**Key Features:**
- **Plant Disease Detection:** Uses Deep Learning (Convolutional Neural Network with PyTorch) to classify leaf images into 39 disease categories, trained on the Plant Village dataset.
- **Thermal Imaging for Irrigation:** Helps manage irrigation using thermal data.
- **Weather Forecasting:** Provides weather updates to optimize farming decisions.
- **Supplement Recommendations:** Suggests fertilizers and supplements based on crop and disease.

---

## ⭐ Getting Started

### Prerequisites
- **Python 3.8** must be installed on your machine.

### Setup Instructions

1. **Create and Activate a Python Virtual Environment**  
   [Python venv guide](https://docs.python.org/3/tutorial/venv.html)

2. **Install Dependencies**  
   ```
   pip install -r requirements.txt
   ```

3. **Download Pre-trained Model**  
   - Download `plant_disease_model_1_latest.pt` from [Google Drive](https://drive.google.com/drive/folders/1ewJWAiduGuld_9oGSrTuLumg9y62qS6A?usp=share_link)
   - Place the file in the `Flask App` folder.

4. **Run the Flask Application**  
   ```
   cd Flask App
   python3 app.py
   ```

5. **(Optional) Use the Model in Jupyter Notebook**  
   - You can also use the downloaded model file in the `Model` section and experiment with it in a Jupyter Notebook.

---

## ⭐ Contribution (Open Source)

- This project is open source—contributions are welcome!
- You can improve the UI, enhance the deep learning model, or add documentation.
- If you update the deep learning model, upload the updated `.md`, `.pdf`, and `.ipynb` files in the appropriate section.
- Ensure your code is error-free and tested before making a pull request.
- **How to contribute:**  
  1. Fork this repository.
  2. Make your changes and test them.
  3. Submit a pull request.  
  [How to make a pull request](https://opensource.com/article/19/7/create-pull-request-github)

---

## ⭐ Testing Images

- Sample leaf images are available in the `test_images` folder.
- Each image is labeled with its disease name for easy verification.

---

## ⭐ Blog

Read more about the project:  
[Plant Disease Detection Using Convolutional Neural Networks with PyTorch](https://medium.com/analytics-vidhya/plant-disease-detection-using-convolutional-neural-networks-and-pytorch-87c00c54c88f)

---

## ⭐ Deployed App

Try the live demo:  
[Plant-Disease-Detection-AI (Heroku)](https://plant-disease-detection-ai.herokuapp.com/)

---

## ⭐ Web App Preview

#### Main Page
<img src="demo_images/1.png" alt="Main Page"><br>
#### Feauture
<img src="demo_images/2.png" alt="Features"><br>
#### AI Engine
<img src="demo_images/6.png" alt="AI Engine"><br>
#### Disease Detection
<img src="demo_images/8.png" alt="Disease Detection"><br>
#### Irrigation Analysis
<img src="demo_images/13.png" alt="Irigation Analysis"><br>
#### Irrigation Analysis
<img src="demo_images/14.png" alt="Irigation Analysis"><br>
#### Supplements/Fertilizer Store
<img src="demo_images/10.JPG" alt="Supplements Store"><br>
#### Weather Section
<img src="demo_images/16.png" alt="Weather Section"><br>
#### Weather Section
<img src="demo_images/15.png" alt="Weather Section"><br><br>