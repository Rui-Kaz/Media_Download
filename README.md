# 🎬 Media Download - Video & Audio Downloader

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A modern, user-friendly desktop application for downloading videos and audio from various online platforms including YouTube, Facebook, Instagram, TikTok, Twitter, and many more.

![Application Screenshot](screenshot.png)

## ✨ Features

### v2.0 - Social Media Resizing �
- 📱 **Video Resizing**: Optimize videos for 10 social media platforms
  - Instagram (Feed, Story, Reels)
  - TikTok, YouTube Shorts
  - Facebook, Twitter/X, LinkedIn
- ✂️ **Smart Resize**: Maintains aspect ratio with intelligent padding
- 🎬 **FFmpeg Embedded**: Works standalone without external dependencies

### Core Features
- �🎥 **Video Download**: Download videos in MP4 format (best quality available)
- 🎵 **Audio Extraction**: Download audio-only in M4A/WEBM format
- 📊 **Real-time Progress**: Visual progress bar with percentage, speed, and ETA
- 🌐 **Multi-platform Support**: Works with YouTube, Facebook, Instagram, TikTok, Twitter, and 1000+ sites
- 🎯 **Single Video Mode**: Downloads only the specific video, not entire playlists (v2.0.1)
- 🎨 **Modern UI**: Clean, intuitive interface following modern HCI principles
- 📁 **Smart Downloads**: Automatically saves to your Downloads folder
- 🚀 **Standalone Executable**: No Python installation required for end users

## 🖥️ Screenshots

### Main Interface
The application features a clean, modern interface with:
- URL input with paste and clear buttons
- Video/Audio selection radio buttons
- Real-time progress tracking
- Quick access to downloads folder

## 🚀 Quick Start

### For End Users (Windows)

1. Download the latest release from [Releases](https://github.com/Rui-Kaz/Media_Download/releases)
2. Run `DescarregadorVideos.exe`
3. Paste a video URL
4. Choose Video or Audio
5. Click Download!

No installation or Python required!

### For Developers

#### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rui-Kaz/Media_Download.git
cd Media_Download
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python saca_videos.py
```

## 📦 Building Executable

To create a standalone Windows executable:

### Option 1: Using Batch File (Easiest)
```bash
compilar.bat
```

### Option 2: Using Python Script
```bash
python build_exe.py
```

### Option 3: Manual PyInstaller
```bash
pyinstaller --name=DescarregadorVideos --onefile --windowed --clean --collect-all=yt_dlp saca_videos.py
```

The executable will be created in the `dist` folder.

## 🎯 Supported Platforms

This application can download from 1000+ websites including:

- **Video Platforms**: YouTube, Vimeo, Dailymotion
- **Social Media**: Facebook, Instagram, TikTok, Twitter
- **Streaming**: Twitch clips, Reddit videos
- And many more!

For a complete list, visit [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## 🛠️ Technical Details

### Built With
- **Python** - Core programming language
- **Tkinter** - GUI framework
- **yt-dlp** - Media download engine
- **PyInstaller** - Executable packaging

### Project Structure
```
Media_Download/
├── saca_videos.py          # Main application
├── build_exe.py            # Build script for executable
├── compilar.bat            # Windows batch build script
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── README_BUILD.md         # Detailed build instructions
├── COMO_COMPILAR.txt       # Build guide (Portuguese)
└── dist/                   # Generated executables (after build)
```

### Features Breakdown

#### Video Download
- Downloads in MP4 format when available
- Automatically selects best quality
- Fallback to alternative formats if needed
- No ffmpeg required for basic downloads

#### Audio Download
- Extracts audio stream without video
- Saves in native format (M4A/WEBM)
- Smaller file sizes
- Faster downloads
- Compatible with all modern media players

#### Progress Tracking
- Real-time percentage display
- Download speed indicator
- Estimated time remaining
- Visual color-coded progress bar:
  - 🔴 Red (0-30%): Starting
  - 🟠 Orange (30-70%): In progress
  - 🟢 Green (70-100%): Almost complete

## 📋 Requirements

### Runtime (for .exe)
- Windows 7 or higher
- ~50 MB disk space

### Development
- Python 3.10+
- Libraries listed in `requirements.txt`

## 🔧 Configuration

The application automatically:
- Detects your Downloads folder
- Manages file naming to avoid conflicts
- Handles various video formats
- Provides fallback options

No manual configuration needed!

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Check antivirus settings (may flag as false positive)
- Run as administrator
- Ensure Windows is up to date

**Download fails**
- Verify the URL is correct and accessible
- Check your internet connection
- Some sites may require authentication
- Try with a different video

**Slow download speed**
- Depends on your internet connection
- Server speed varies by platform
- Large videos take longer

**Antivirus warning**
- This is a false positive common with PyInstaller
- Add an exception in your antivirus
- Source code is available for verification

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful media download library
- [PyInstaller](https://www.pyinstaller.org/) - Executable packaging
- Python Software Foundation - Python language

## 📧 Contact

Rui Kaz - [@Rui-Kaz](https://github.com/Rui-Kaz)

Project Link: [https://github.com/Rui-Kaz/Media_Download](https://github.com/Rui-Kaz/Media_Download)

## ⚖️ Legal Disclaimer

This tool is for personal use only. Please respect copyright laws and terms of service of the platforms you download from. The developers are not responsible for any misuse of this software.

---

**Made with ❤️ using Python**
