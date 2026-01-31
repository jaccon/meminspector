# 🔍 MemInspector

Memory Inspector for macOS - A powerful tool to analyze memory consumption of applications and threads with beautiful visualizations.

## ✨ Features

- 📊 **Real-time Process Monitoring** - Track memory usage of all running processes
- 🎨 **Beautiful Terminal UI** - Colored, interactive terminal interface
- 📉 **Interactive Graphs** - matplotlib-powered real-time visualization
- 🐳 **Docker Support** - Monitor container memory consumption
- 🧵 **Thread Analysis** - Detailed thread information for each process
- 💻 **System Statistics** - Complete memory and swap information
- 🔄 **Auto-refresh Mode** - Continuous monitoring with customizable intervals
- 📈 **ASCII Graphs** - Terminal-based memory usage charts

## 📦 Installation

### Option 1: Homebrew (Recommended for macOS)

```bash
# Add the tap (first time only)
brew tap jaccon/tap

# Install meminspector
brew install jaccon/tap/meminspector

# Or in one command
brew install jaccon/tap/meminspector
```

### Option 2: Via pip

```bash
pip install git+https://github.com/jaccon/meminspector.git
```

### Option 3: Manual Installation

```bash
git clone https://github.com/jaccon/meminspector.git
cd meminspector
pip install -e .
```

**Dependencies (installed automatically):**

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Interactive colored terminal UI (recommended)
meminspector --tui

# Real-time graphs with matplotlib
meminspector --graph

# Continuous refresh mode
meminspector --refresh

# List all processes (single snapshot)
meminspector --list

# Show top 30 processes in TUI
meminspector --tui -t 30

# Graphs with custom refresh interval
meminspector --graph -t 15 -i 1
```

## 📖 Usage

### Command Line Options

```
OPTIONS:
    -h, --help              Show help message
    -l, --list              List all processes (default mode)
    --tui                   Colored terminal interface (recommended)
    -r, --refresh           Continuous refresh mode
    -g, --graph             Show interactive matplotlib graphs
    -t, --top N             Number of top processes to show (default: 20)
    -i, --interval N        Update interval in seconds (default: 2.0)
    -a, --analyze N         Number of processes to analyze threads (default: 5)
```

### Usage Modes

#### 1. Terminal UI Mode (Recommended)
Beautiful, colored interface with real-time updates:

```bash
meminspector --tui
meminspector --tui -t 30        # Show top 30 processes
meminspector --tui -i 1         # Update every second
```

Features:
- Color-coded memory usage
- Live system statistics
- Docker container monitoring (if available)
- ASCII memory trend graph
- Keyboard navigation (q or ESC to quit)

#### 2. Graph Mode
Interactive matplotlib visualizations:

```bash
meminspector --graph
meminspector -g -t 15           # Top 15 processes
meminspector -g -i 3            # Update every 3 seconds
```

Displays:
- System memory usage over time
- Top N processes by memory consumption
- Real-time updates

#### 3. Refresh Mode
Continuous terminal updates:

```bash
meminspector --refresh
meminspector -r -t 20 -i 5      # Top 20, refresh every 5s
```

#### 4. List Mode
Single snapshot of all processes:

```bash
meminspector
meminspector --list
meminspector -l -a 10           # Analyze threads of top 10
```

## 📊 Screenshots

### Terminal UI Mode
```
╭─────────────────────────────────────────────────────────────╮
│ MemInspector | 2026-01-31 15:30:45 | Total Processes: 342 │
╰─────────────────────────────────────────────────────────────╯

╭─ Top 20 Processes by Memory Usage ─────────────────────────╮
│ #   PID      Name                     Memory      %        │
│ 1   1234     Google Chrome            2.45 GB    15.20%   │
│ 2   5678     Docker Desktop           1.82 GB    11.30%   │
│ 3   9012     VSCode                   1.45 GB     9.00%   │
│ ...                                                        │
╰────────────────────────────────────────────────────────────╯

╭─ System Memory ────────────────────────────────────────────╮
│ Total Memory      16.00 GB                                 │
│ Used Memory       12.45 GB (77.8%)  ████████████████░░░░░  │
│ Available         3.55 GB                                  │
╰────────────────────────────────────────────────────────────╯
```

### Graph Mode
Real-time matplotlib graphs showing:
- Memory usage trends over time
- Top processes comparison
- System statistics

## 🐳 Docker Support

MemInspector automatically detects and monitors Docker containers if Docker is running:

```bash
# Docker will be monitored automatically in TUI mode
meminspector --tui
```

Requirements:
- Docker Desktop running
- `docker` Python package installed (`pip install docker`)

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/jaccon/meminspector.git
cd meminspector

# Install in development mode
pip install -e .

# Run directly from source
python3 meminspector.py --tui

# Install dev dependencies
pip install -r requirements.txt
```

## 📋 Requirements

- Python 3.7+
- macOS (primary support) or Linux
- Dependencies:
  - `psutil` - Process and system monitoring
  - `rich` - Terminal UI components
  - `tqdm` - Progress bars
  - `matplotlib` - Graph visualization (optional)
  - `docker` - Docker monitoring (optional)

## 🐛 Troubleshooting

### Permission Errors

Some system processes require elevated privileges:

```bash
sudo meminspector --tui
```

### Missing matplotlib

If graphs don't work:

```bash
pip install matplotlib
```

### Docker Connection Issues

If Docker monitoring fails:
- Make sure Docker Desktop is running
- Install docker package: `pip install docker`
- Check Docker daemon: `docker ps`

### Import Errors

Install all dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Use Cases

- **Development** - Monitor memory leaks during development
- **DevOps** - Track container memory usage
- **System Admin** - Identify memory-hungry processes
- **Performance Testing** - Analyze application memory consumption
- **Learning** - Understand system resource usage

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Developed by Jaccon**
- GitHub: [@jaccon](https://github.com/jaccon)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [psutil](https://github.com/giampaolo/psutil)
- UI powered by [rich](https://github.com/Textualize/rich)
- Graphs using [matplotlib](https://matplotlib.org/)

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**⭐ If you find this tool useful, please give it a star on GitHub!**
