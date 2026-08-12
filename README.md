# WLV-MSc-AI

I will be using the following Python environment for my MSc in Artificial Intelligence at the University of Wolverhampton (WLV). This environment, named WLV-AI, is built on Conda and includes essential Data Science and Machine Learning libraries such as NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, TensorFlow, PyTorch, Jupyter, the IPython kernel, and SciPy. The workflow is designed to ensure reproducibility of dependencies through the use of an [environment.yml](https://github.com/santiago-cruzlopez/WLV-MSc-AI/blob/master/environment.yml) file.

- [Anaconda Documentation](https://www.anaconda.com/docs/main)

## Modules
1. [7CS074/UZ2: Data Mining & Informatics](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/01_Data_Mining_%26_Informatics)
2. [7CS082/UZ3: Deep Machine Learning](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/02_Deep_Machine_Learning)
3. [7CS083/UZ2:Intelligent Agents](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/03_Intelligent_Agents)
4. [7CS075/UZ1: Research Methods](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/04_Research_Methods)
5. [7CS084/UZ2: Applying Artificial Intelligence](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/05_Applying_Artificial_Intelligence)
6. [7CS071/UZ1: Virtualization and Cloud Computing](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/06_Cloud_Computing)
7. [7CS070/UZ2: Concepts & Technologies of Artificial Intelligence](https://github.com/santiago-cruzlopez/WLV-MSc-AI/tree/master/07_Concepts_%26_Technologies_of_Artificial_Intelligence)

## Core Installation Steps

1. System Dependencies and Packages (Ubuntu 22.04):
    - Update package information and install the required packages:
      ```bash
      sudo apt update && sudo apt upgrade
      sudo apt-get install -y build-essential pkg-config cmake make unzip yasm dkms git checkinstall libsdl2-dev libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev
      sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
      ```
    - Install Miniconda on Ubuntu 22.04 - [Instructions](https://docs.conda.io/en/latest/miniconda.html):
      ```bash
      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
      sha256sum Miniconda3-latest-Linux-x86_64.sh
      
      # Run the installer 
      bash Miniconda3-latest-Linux-x86_64.sh
      source ~/.bashrc

      # Control whether or not your shell has the base environment activated each time it opens
      conda config --set auto_activate_base True
      conda config --set auto_activate_base False

      # Verify Installation
      conda info
      conda env list
      conda --version
      ```

2. Ubuntu Python Environment Setup
    - Create the environment with Python 3.10 and common ML/data science libraries:
      ```bash
      conda create -n WLV-AI python=3.10 numpy=1.26.4 pandas matplotlib seaborn scikit-learn pytorch jupyter ipykernel scipy -c pytorch -c conda-forge -y
      conda activate WLV-AI
      pip install kagglehub
      # Install Jupyter kernel
      python -m ipykernel install --user --name WLV-AI --display-name "WLV-AI"

      conda env export > environment.yml
      conda list
      ```
    - Install TensorFlow with GPU Support
      ```bash
      pip install --upgrade pip setuptools wheel
      pip install 'tensorflow[and-cuda]==2.15.*'
      pip install --upgrade absl-py  # Fixes Abseil symbol errors

      # Verify TF Installation
      import tensorflow as tf
      print(tf.__version__)
      print(tf.config.list_physical_devices('GPU'))
      ```
    - Creating a TensorFlow GPU Environment
      ```bash
      conda create -n WLV-TF python=3.10 -y
      conda activate WLV-TF

      conda install numpy=1.26.4 pandas matplotlib seaborn scikit-learn scipy jupyter ipykernel -y

      pip install --upgrade pip setuptools wheel
      pip install 'tensorflow[and-cuda]==2.15.*'
      pip install --upgrade absl-py

      python -m ipykernel install --user --name WLV-TF --display-name "WLV-TF"

      # Verify GPU 
      python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
      ```
3. Windows 10/11 Conda Env:
    - Install Miniconda on Windows 10/11 - [Instructions](https://docs.conda.io/en/latest/miniconda.html):
      ```bash
      conda --version
      conda info --envs
      conda list
      ```
    - Open the **Anaconda Prompt** from your Windows Start Menu and run the following commands sequentially:
      ```cmd
      # 1. Accept Anaconda's Terms of Service for repository channels
      conda tos accept --override-channels --channel https://anaconda.com
      conda tos accept --override-channels --channel https://anaconda.com
      conda tos accept --override-channels --channel https://anaconda.com

      # 2. Create a clean Python 3.10 deployment sandbox
      conda create -n WLV-AI python=3.10 -y

      # 3. Activate the new workspace
      conda activate WLV-AI

      # 4. Install the core Data Science & Analysis framework via standard channels
      conda install numpy=1.26.4 pandas matplotlib seaborn scikit-learn scipy statsmodels jupyter ipykernel -y

      # 5. Upgrade execution and deployment tools via Python runtime module
      python -m pip install --upgrade pip setuptools wheel

      # 6. Install TensorFlow 2.15 and Hidden Markov Models package via Pip
      pip install tensorflow==2.15.* hmmlearn absl-py

      # 7. Bind your new execution kernel cleanly to Jupyter Notebook
      python -m ipykernel install --user --name WLV-AI --display-name "WLV-AI"

      # 8. Verify the Python environment and installed packages
      conda list

      python -c "import numpy as np; import pandas as pd; import tensorflow as tf; import hmmlearn; print('--- SYSTEM STATUS ---'); print('NumPy:', np.__version__); print('Pandas:', pd.__version__); print('TensorFlow:', tf.__version__); print('All systems nominal!')"
      ```
