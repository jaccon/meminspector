import Foundation

enum Mode {
    case list, tui, refresh, graph
}

struct CommandLineArgs {
    var mode: Mode = .list
    var topN: Int = 20
    var interval: Double = 2.0
    var showHelp: Bool = false
}

func parseArguments() -> CommandLineArgs {
    var args = CommandLineArgs()
    let arguments = CommandLine.arguments
    
    var i = 1
    while i < arguments.count {
        let arg = arguments[i]
        
        switch arg {
        case "-h", "--help": args.showHelp = true
        case "-l", "--list": args.mode = .list
        case "--tui": args.mode = .tui
        case "-r", "--refresh": args.mode = .refresh
        case "-g", "--graph": args.mode = .graph
        case "-t", "--top":
            if i + 1 < arguments.count, let value = Int(arguments[i + 1]) {
                args.topN = value
                i += 1
            }
        case "-i", "--interval":
            if i + 1 < arguments.count, let value = Double(arguments[i + 1]) {
                args.interval = value
                i += 1
            }
        default: break
        }
        i += 1
    }
    return args
}

func printHelp() {
    print("""
    MemInspector - Memory Inspector for macOS (Swift Native)

    USAGE:
        meminspector [OPTIONS]

    OPTIONS:
        -h, --help              Show this help message
        -l, --list              List all processes by memory usage (default mode)
        --tui                   Colored terminal user interface (recommended)
        -r, --refresh           Continuous refresh mode in terminal
        -g, --graph             Show ASCII graphs
        -t, --top N             Number of top processes to show (default: 20)
        -i, --interval N        Update interval in seconds for refresh mode (default: 2.0)

    EXAMPLES:
        meminspector                    # List all processes (default)
        meminspector --list             # List all processes
        meminspector --tui              # Colored terminal interface (recommended)
        meminspector --tui -t 30        # TUI with top 30 processes
        meminspector --refresh          # Continuous refresh in terminal
        meminspector -r -t 20 -i 3      # Refresh top 20 every 3 seconds
        meminspector --graph -t 15      # Show ASCII graphs with top 15 processes

    FEATURES:
        • Native Swift implementation - no dependencies required
        • Real-time memory monitoring
        • Process and thread information  
        • System memory statistics
        • Colored terminal output
        • ASCII graphs

    Developed by Jaccon
    """)
}

func runListMode(topN: Int?) {
    let monitor = ProcessMonitor()
    
    TerminalUI.printHeader("MemInspector - Memory Inspector for macOS")
    
    if let systemInfo = monitor.getSystemMemoryInfo() {
        TerminalUI.printSystemSummary(systemInfo)
    }
    
    print("Collecting process information...\n")
    let processes = monitor.getAllProcesses()
    
    if let top = topN {
        TerminalUI.printProcessTable(processes, topN: top)
    } else {
        TerminalUI.printProcessTable(processes)
    }
    
    print("Total processes: \(TerminalUI.colored("\(processes.count)", color: .green))")
    print()
}

func runTUIMode(topN: Int, interval: Double) {
    let monitor = ProcessMonitor()
    
    TerminalUI.clearScreen()
    TerminalUI.printHeader("MemInspector - Colored Terminal UI")
    
    if let systemInfo = monitor.getSystemMemoryInfo() {
        TerminalUI.printSystemSummary(systemInfo)
        
        TerminalUI.printMemoryBar(
            label: "Memory Usage",
            used: systemInfo.usedMemory,
            total: systemInfo.totalMemory
        )
        print()
    }
    
    let processes = monitor.getAllProcesses()
    TerminalUI.printProcessTable(processes, topN: topN)
    TerminalUI.printASCIIGraph(processes, topN: min(topN, 10))
    
    print(TerminalUI.colored("\nPress Ctrl+C to exit", color: .yellow))
    print(TerminalUI.colored("Developed by Jaccon", color: .cyan))
}

func runRefreshMode(topN: Int, interval: Double) {
    signal(SIGINT) { _ in
        print("\n\nExiting...\n")
        exit(0)
    }
    
    print("Starting continuous refresh mode (Ctrl+C to exit)...\n")
    
    while true {
        TerminalUI.clearScreen()
        runTUIMode(topN: topN, interval: interval)
        sleep(UInt32(interval))
    }
}

func runGraphMode(topN: Int) {
    let monitor = ProcessMonitor()
    
    TerminalUI.printHeader("MemInspector - ASCII Graph Mode")
    
    if let systemInfo = monitor.getSystemMemoryInfo() {
        TerminalUI.printSystemSummary(systemInfo)
        
        TerminalUI.printMemoryBar(
            label: "Total Memory",
            used: systemInfo.usedMemory,
            total: systemInfo.totalMemory,
            width: 70
        )
        print()
    }
    
    let processes = monitor.getAllProcesses()
    TerminalUI.printASCIIGraph(processes, topN: topN)
    TerminalUI.printProcessTable(processes, topN: topN)
}
