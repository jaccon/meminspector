# 🔍 MemInspector

Memory Inspector for macOS - A powerful tool to analyze memory consumption of applications and threads.

> **NEW:** Swift native version available with **zero dependencies** and **93KB binary size**! 🚀

## 🌟 Two Versions Available

### 🦅 Swift Native Version (Recommended)
- ✅ **Zero dependencies** - Native macOS binary
- ✅ **High performance** - ~10ms startup time
- ✅ **Tiny binary** - Only 93KB
- ✅ **Native APIs** - Direct system integration
- ✅ **Easy distribution** - Single executable

### 🐍 Python Version
- ✅ **Rich features** - matplotlib graphs, Docker monitoring
- ✅ **Cross-platform** - Works on any OS with Python
- ✅ **Extensible** - Easy to customize

## 📦 Installation

### Swift Version (Recommended for macOS users)

**Quick Install (requires Swift compiler):**

```bash
curl -fsSL https://raw.githubusercontent.com/jaccon/meminspector/main/swift-version/install.sh | bash
```

**Manual Build:**

```bash
git clone https://github.com/jaccon/meminspector.git
cd meminspector/swift-version
swift build -c release
sudo cp .build/release/MemInspector /usr/local/bin/meminspector
```

**Requirements:**
- Swift compiler (install with `xcode-select --install` or Xcode.app)
- macOS 12.0 or later

### Python Version

**Via Homebrew:**

```bash
brew install jaccon/tap/meminspector
```

**Via pip:**

```bash
pip install git+https://github.com/jaccon/meminspector.git
```

**Manual:**

```bash
git clone https://github.com/jaccon/meminspector.git
cd meminspector
pip install -e .
```

## 🚀 Quick Start

```bash
# List all processes
meminspector

# Colored terminal UI (recommended)
meminspector --tui

# Continuous refresh mode
meminspector --refresh

# ASCII graphs
meminspector --graph -t 15

# Show top 30 processes
meminspector --tui -t 30
```

## 📊 Features

### Common Features (Both Versions)
- 📊 Process memory usage sorted by consumption
- 🧵 Thread information for each process
- 💻 System memory statistics (total, available, swap)
- 🎨 Colored terminal output
- 🔄 Real-time refresh mode
- 📈 ASCII progress bars and graphs

### Python Version Only
- 📉 Interactive matplotlib graphs
- 🐳 Docker container monitoring
- 🔍 Advanced thread analysis

### Swift Version Only
- ⚡ Native performance (~10ms startup)
- 📦 No dependencies required
- 🪶 Ultra-small binary (93KB)
- 🍎 Direct macOS API access

## 📖 Usage

### Command Line Options

```
OPTIONS:
    -h, --help              Show help message
    -l, --list              List all processes (default mode)
    --tui                   Colored terminal interface (recommended)
    -r, --refresh           Continuous refresh mode
    -g, --graph             Show graphs (ASCII for Swift, matplotlib for Python)
    -t, --top N             Number of top processes to show (default: 20)
    -i, --interval N        Update interval in seconds (default: 2.0)
```

### Examples

```bash
# List all processes
meminspector
meminspector --list

# Colored TUI mode
meminspector --tui
meminspector --tui -t 30        # Top 30 processes

# Continuous refresh
meminspector --refresh
meminspector -r -t 20 -i 3      # Top 20, refresh every 3s

# Graphs
meminspector --graph
meminspector -g -t 15           # Top 15 with graphs
```

## 🆚 Version Comparison

| Feature | Swift Native | Python |
|---------|-------------|---------|
| **Startup Time** | ~10ms | ~500ms |
| **Memory Usage** | ~5MB | ~50MB |
| **Binary Size** | 93KB | N/A (interpreter) |
| **Dependencies** | 0 | 5+ packages |
| **Installation** | Single binary | pip/brew |
| **Performance** | Native | Interpreted |
| **matplotlib Graphs** | ❌ (ASCII only) | ✅ |
| **Docker Monitoring** | ❌ | ✅ |
| **Platform** | macOS only | Cross-platform |

## 🛠️ Development

### Swift Version

```bash
cd swift-version

# Build
swift build

# Run
swift run

# Release build
swift build -c release

# Test
.build/release/MemInspector --tui
```

### Python Version

```bash
# Install in development mode
pip install -e .

# Run directly
python3 meminspector.py --tui
```

## 📝 Technical Details

### Swift Version Architecture
- Uses native Darwin/Mach APIs
- Direct access to `task_info`, `vm_statistics64`
- Process enumeration via `proc_listallpids`
- Thread counting with `task_threads`
- Zero external dependencies

### Python Version Architecture
- Built on `psutil` for system info
- `rich` for terminal UI
- `matplotlib` for interactive graphs (optional)
- `docker` for container monitoring (optional)

## 🐛 Troubleshooting

### Permission Errors

Some system processes require elevated privileges:

```bash
# Python version
sudo meminspector

# Swift version
sudo meminspector
```

### Swift Version Not Found

Make sure the binary is in your PATH:

```bash
# Check installation
which meminspector

# Manual installation
cp .build/release/MemInspector /usr/local/bin/meminspector
chmod +x /usr/local/bin/meminspector
```

### Python Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Core dependencies only (without matplotlib)
pip install psutil tqdm rich docker
```

## 🎯 Which Version Should I Use?

**Use Swift Native if you want:**
- ✅ Maximum performance
- ✅ No dependencies to manage
- ✅ Smallest footprint
- ✅ macOS-only usage

**Use Python if you need:**
- ✅ Interactive matplotlib graphs
- ✅ Docker container monitoring
- ✅ Cross-platform support
- ✅ Easy customization

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Developed by Jaccon**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**⭐ If you find this tool useful, please give it a star on GitHub!**
