# Installation Guide

## For End Users

### Windows
1. Go to [Releases](https://github.com/Rui-Kaz/Media_Download/releases)
2. Download `DescarregadorVideos.exe`
3. Run the executable
4. No installation needed!

## For Developers

### Prerequisites
- Python 3.10 or higher
- pip (included with Python)
- Git (for cloning)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/Rui-Kaz/Media_Download.git
cd Media_Download
```

#### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
python saca_videos.py
```

### Building Executable

#### Windows
```bash
# Option 1: Batch file
compilar.bat

# Option 2: Python script
python build_exe.py

# Option 3: Manual
pyinstaller --name=DescarregadorVideos --onefile --windowed --collect-all=yt_dlp saca_videos.py
```

The executable will be in the `dist` folder.

### Development Tools

#### Recommended IDE
- Visual Studio Code
- PyCharm
- Any Python-compatible editor

#### Useful Extensions (VS Code)
- Python
- Pylance
- GitLens

### Troubleshooting

#### "Python not found"
- Ensure Python is installed and in PATH
- Try `python3` instead of `python`

#### "Module not found"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

#### "Permission denied"
- Run as administrator (Windows)
- Use `sudo` (Linux/Mac) if needed

### Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check [README.md](README.md) for feature documentation
- Review code structure in `saca_videos.py`

### Support

If you encounter issues:
1. Check existing [Issues](https://github.com/Rui-Kaz/Media_Download/issues)
2. Create a new issue with details
3. Include error messages and system info
