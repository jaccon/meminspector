# Quick Start for Homebrew Packaging

## Summary

To publish MemInspector via Homebrew, follow these steps:

### 1. Prepare Repository
```bash
# Update setup.py with your information (already done for v1.1.0)
# Version: 1.1.0
# Author: Jaccon
# URL: github.com/jaccon/meminspector

# Commit all changes
git add .
git commit -m "Version 1.1.0 - TUI and Docker support"
```

### 2. Create GitHub Release
```bash
# Tag the version
git tag -a v1.1.0 -m "Version 1.1.0 - TUI and Docker support"
git push origin main
git push origin v1.1.0

# Create release on GitHub
# Go to: https://github.com/jaccon/meminspector/releases/new
# - Tag: v1.1.0
# - Title: Version 1.1.0 - TUI and Docker Support
# - Description: See CHANGELOG.md
```

### 3. Calculate SHA256
```bash
# Download the release tarball
curl -L https://github.com/jaccon/meminspector/archive/refs/tags/v1.1.0.tar.gz -o meminspector.tar.gz

# Get SHA256
shasum -a 256 meminspector.tar.gz
```

### 4. Update Formula
Edit `meminspector.rb`:
- Already updated to v1.1.0
- URL points to github.com/jaccon/meminspector
- Replace `YOUR_SHA256_HASH_HERE` with the actual SHA256 hash
- Includes all dependencies: psutil, tqdm, matplotlib, rich, docker

### 5. Create Homebrew Tap
```bash
# On GitHub, create a new repository named: homebrew-tap

# Clone it locally
git clone https://github.com/jaccon/homebrew-tap.git
cd homebrew-tap

# Create Formula directory
mkdir Formula

# Copy the formula
cp /path/to/meminspector/meminspector.rb Formula/

# Commit and push
git add .
git commit -m "Add meminspector v1.1.0 formula"
git push origin main
```

### 6. Test Installation
```bash
# Test locally first
brew install --build-from-source /path/to/meminspector.rb

# Test the command
meminspector --help
meminspector --tui

# If it works, uninstall and test from tap
brew uninstall meminspector

# Install from your tap
brew tap jaccon/tap
brew install meminspector
```

### 7. Share with Users
Users can now install with:
```bash
brew tap jaccon/tap
brew install meminspector
```

## Important Files Checklist

- [x] `meminspector.py` - Main application (v1.1.0 with TUI and Docker)
- [x] `setup.py` - Package configuration (v1.1.0, author: Jaccon)
- [x] `requirements.txt` - Dependencies (includes rich and docker)
- [x] `README.md` - Documentation
- [x] `LICENSE` - MIT License
- [x] `meminspector.rb` - Homebrew formula (v1.1.0 with all resources)
- [x] `HOMEBREW_GUIDE.md` - Detailed guide
- [x] `CHANGELOG.md` - Version history

## What's New in v1.1.0

- **Colored TUI Interface** - Beautiful terminal interface with Rich
- **Docker Support** - Monitor Docker containers memory usage
- **Keyboard Controls** - Press 'q' or 'ESC' to exit
- **Better Error Handling** - Improved Docker connection and error messages
- **Footer Credits** - "Developed by Jaccon"

## Next Steps After Setup

1. ✅ Update `setup.py` with your personal information (DONE)
2. ✅ Update formula with new dependencies (DONE)
3. Create GitHub repository at github.com/jaccon/meminspector
4. Push all code
5. Create release tag v1.1.0
6. Calculate SHA256
7. Update formula file with SHA256
8. Create tap repository at github.com/jaccon/homebrew-tap
9. Test installation
10. Share installation instructions

For detailed information, see [HOMEBREW_GUIDE.md](HOMEBREW_GUIDE.md)
