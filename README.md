# WLV-MSc-AI

I will be using the following Python environment for my MSc in Artificial Intelligence at the University of Wolverhampton (WLV). This environment, named WLV-AI, is built on Conda and includes essential Data Science and Machine Learning libraries such as NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, TensorFlow, PyTorch, Jupyter, the IPython kernel, and SciPy. The workflow is designed to ensure reproducibility of dependencies through the use of an [environment.yml](https://github.com/santiago-cruzlopez/WLV-MSc-AI/blob/master/environment.yml) file.

## Modules
1. 7CS074/UZ2: Data Mining & Informatics
2. 7CS082/UZ3: Deep Machine Learning

## Core Installation Steps

1. System Dependencies and Packages
  - Update package information and install the required packages:
  ```bash
  sudo apt update && sudo apt upgrade
  sudo apt-get install -y build-essential pkg-config cmake make unzip yasm dkms git checkinstall libsdl2-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev
  ```
  - Install Anaconda
  ```bash
  wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh -O Anaconda3-latest-Linux-x86_64.s
  
  # Run the installer 
  bash Anaconda3-latest-Linux-x86_64.sh

  # Verify Installation
  conda --version
  anaconda-navigator
  ```

2. Python Environment Setup
  - Create the environment with Python 3.10 and common ML/data science libraries:
  ```bash
  conda create -n WLV-AI python=3.10 numpy pandas matplotlib seaborn scikit-learn tensorflow pytorch jupyter ipykernel scipy -y

  conda activate WLV-AI
  conda env export > environment.yml

  conda list
  ```
