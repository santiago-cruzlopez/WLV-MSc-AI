# WLV-MSc-AI

I will be using the following Python environment for my MSc in Artificial Intelligence at the University of Wolverhampton (WLV). This environment, named WLV-AI, is built on Conda and includes essential Data Science and Machine Learning libraries such as NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, TensorFlow, PyTorch, Jupyter, the IPython kernel, and SciPy. The workflow is designed to ensure reproducibility of dependencies through the use of an [environment.yml](https://github.com/santiago-cruzlopez/WLV-MSc-AI/blob/master/environment.yml) file.

- [Anaconda Documentation](https://www.anaconda.com/docs/main)

## Modules
1. [7CS074/UZ2: Data Mining & Informatics](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/01_Data_Mining_%26_Informatics)
2. [7CS082/UZ3: Deep Machine Learning](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/02_Deep_Machine_Learning)

## Core Installation Steps

1. System Dependencies and Packages
  - Update package information and install the required packages:
  ```bash
  sudo apt update && sudo apt upgrade
  sudo apt-get install -y build-essential pkg-config cmake make unzip yasm dkms git checkinstall libsdl2-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev
  sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
  ```
  - Install Anaconda on Ubuntu 22.04 - [Instructions](https://www.geeksforgeeks.org/linux-unix/how-to-install-anaconda-on-ubuntu-20-04/):
  ```bash
  wget https://repo.anaconda.com/archive/Anaconda3-2025.12-1-Linux-x86_64.sh
  # or
  curl -O https://repo.anaconda.com/archive/Anaconda3-2025.12-1-Linux-x86_64.sh
  
  # Run the installer 
  bash Anaconda3-2025.12-1-Linux-x86_64.sh

  # Control whether or not your shell has the base environment activated each time it opens
  conda config --set auto_activate_base True
  conda config --set auto_activate_base False

  # Verify Installation
  conda info
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
