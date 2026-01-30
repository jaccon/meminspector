# 🔍 MemInspector (Swift Native Version)

Native macOS memory inspector written in Swift with zero dependencies.

## 🚀 Features

- ✅ **Native Swift** - No Python or external dependencies
- ✅ **High Performance** - Compiled binary, instant startup
- ✅ **System Integration** - Direct access to macOS APIs
- ✅ **Colored Output** - Beautiful terminal interface
- ✅ **Real-time Monitoring** - Continuous refresh mode
- ✅ **ASCII Graphs** - Visual memory representation
- ✅ **Small Binary** - ~100KB executable

## 📦 Installation

### Option 1: Build from source

```bash
cd swift-version
swift build -c release
cp .build/release/MemInspector /usr/local/bin/meminspector
```

### Option 2: Using Homebrew (Coming soon)

```bash
brew install jaccon/tap/meminspector-swift
```

## 📖 Usage

```bash
# List all processes
meminspector

# Colored TUI mode
meminspector --tui

# Continuous refresh
meminspector --refresh

# ASCII graphs
meminspector --graph -t 15

# Show top 30 processes
meminspector --tui -t 30

# Refresh every 3 seconds
meminspector -r -i 3
```

## 🛠️ Build Requirements

- macOS 12.0 or later
- Xcode 14.0 or later
- Swift 5.7+

## 📊 Performance Comparison

| Metric | Python Version | Swift Version |
|--------|---------------|---------------|
| Startup Time | ~500ms | ~10ms |
| Memory Usage | ~50MB | ~5MB |
| Binary Size | N/A (interpreter) | ~100KB |
| Dependencies | 5+ packages | 0 (native) |

## 🔧 Development

```bash
# Build
swift build

# Run
swift run

# Test
swift test

# Release build
swift build -c release
```

## 📝 Technical Details

### Native APIs Used

- `Darwin.mach` - System statistics and process information
- `Foundation.ProcessInfo` - System memory information  
- `task_info` - Process memory footprint
- `proc_listallpids` - Process enumeration
- `task_threads` - Thread counting

### Features Implemented

- [x] Process memory monitoring
- [x] System memory statistics
- [x] Colored terminal output
- [x] ASCII progress bars
- [x] ASCII graphs
- [x] Real-time refresh mode
- [x] Process sorting by memory
- [x] Thread counting
- [ ] Docker container monitoring (coming soon)
- [ ] Native GUI with SwiftUI (coming soon)

## 🆚 Python vs Swift Version

**Use Python version if you need:**
- matplotlib interactive graphs
- Docker container monitoring
- Cross-platform support

**Use Swift version if you want:**
- Native macOS performance
- No dependencies to install
- Faster startup time
- Smaller memory footprint
- Easier distribution

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

Developed by Jaccon

---

**Note**: This is a native Swift rewrite of the Python MemInspector, optimized for macOS with no external dependencies.
