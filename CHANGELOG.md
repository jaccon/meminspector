# Changelog - MemInspector

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-01-30

### Added
- **Colored Terminal Interface (TUI)** using Rich library
  - Live updating colored interface with panels and tables
  - ASCII graph showing memory usage trend
  - System memory panel with colored progress bars
  - Real-time process monitoring with color-coded memory usage
- **Docker Container Support**
  - Automatic detection of running Docker containers
  - Display container memory usage and statistics
  - Sort containers by memory consumption
  - Shows up to 15 containers in TUI mode
- **Keyboard Controls**
  - Press 'q' or 'ESC' to exit TUI mode
  - Instant key detection without requiring Enter
- **Footer with Credits**
  - Developer attribution in footer
  - GitHub repository link

### Changed
- Improved error handling for Docker connection
- Better memory percentage display (handles None values)
- Simplified Docker table layout (removed ID and Image columns for better readability)
- Increased container display from 10 to 15 in TUI mode

### Fixed
- Fixed TypeError when memory_percent is None
- Improved Docker container name and image detection
- Better terminal settings restoration on exit
- Cache subtraction in Docker memory calculation

## [1.0.0] - 2026-01-30

### Added
- Initial release
- List all processes by memory usage
- Analyze threads of top processes
- System memory summary
- Real-time graph mode with matplotlib
- Continuous refresh mode
- Command-line arguments for customization
- macOS compatibility check
- Progress bars using tqdm

### Features
- Multiple operation modes (list, graph, refresh)
- Configurable update intervals
- Configurable number of top processes to display
- Thread analysis for top processes
- Memory usage formatting (B, KB, MB, GB, TB)
- Graceful error handling

---

## How to Update

### For Users:

If installed via Homebrew:
```bash
brew update
brew upgrade meminspector
```

If installed via pip:
```bash
pip install --upgrade meminspector
```

### For Developers:

To create a new release:

1. Update version in `setup.py` and `meminspector.rb`
2. Create a git tag:
   ```bash
   git tag -a v1.1.0 -m "Version 1.1.0 - TUI and Docker support"
   git push origin v1.1.0
   ```
3. Calculate new SHA256:
   ```bash
   curl -L https://github.com/jaccon/meminspector/archive/refs/tags/v1.1.0.tar.gz | shasum -a 256
   ```
4. Update `meminspector.rb` with the new SHA256
5. Test the formula:
   ```bash
   brew install --build-from-source ./meminspector.rb
   ```
