import Foundation

class TerminalUI {
    enum Color: String {
        case reset = "\u{001B}[0m"
        case red = "\u{001B}[31m"
        case green = "\u{001B}[32m"
        case yellow = "\u{001B}[33m"
        case blue = "\u{001B}[34m"
        case magenta = "\u{001B}[35m"
        case cyan = "\u{001B}[36m"
        case white = "\u{001B}[37m"
        case bold = "\u{001B}[1m"
    }
    
    static func clearScreen() {
        print("\u{001B}[2J\u{001B}[H", terminator: "")
        fflush(stdout)
    }
    
    static func colored(_ text: String, color: Color) -> String {
        return "\(color.rawValue)\(text)\(Color.reset.rawValue)"
    }
    
    static func printHeader(_ title: String) {
        let separator = String(repeating: "=", count: 100)
        print(colored(separator, color: .cyan))
        print(colored(title, color: .bold))
        print(colored(separator, color: .cyan))
        print()
    }
    
    static func printSystemSummary(_ info: SystemMemoryInfo) {
        printHeader("SYSTEM SUMMARY")
        
        print("Total Memory:      \(colored(info.formattedTotal, color: .green))")
        print("Used Memory:       \(colored(info.formattedUsed, color: .yellow)) (\(String(format: "%.1f%%", info.percentUsed)))")
        print("Available Memory:  \(colored(info.formattedAvailable, color: .green))")
        print("Free Memory:       \(colored(info.formattedFree, color: .green))")
        print()
    }
    
    static func printProcessTable(_ processes: [ProcessMemoryInfo], topN: Int? = nil) {
        let displayProcesses = topN.map { Array(processes.prefix($0)) } ?? processes
        
        printHeader("PROCESSES BY MEMORY USAGE (\(displayProcesses.count) processes)")
        
        // Header
        print(colored("#     PID      Name                                 Memory           % Mem      Threads  Status", color: .bold))
        print(String(repeating: "-", count: 100))
        
        // Processes
        for (index, process) in displayProcesses.enumerated() {
            let color: Color = process.memoryPercent > 5.0 ? .red :
                              process.memoryPercent > 2.0 ? .yellow : .white
            
            // Safely truncate and pad name
            let displayName = process.name.count > 35 ? String(process.name.prefix(35)) : process.name
            let paddedName = displayName.padding(toLength: 35, withPad: " ", startingAt: 0)
            let paddedMem = process.formattedMemory.padding(toLength: 15, withPad: " ", startingAt: 0)
            let percentStr = String(format: "%.2f%%", process.memoryPercent).padding(toLength: 10, withPad: " ", startingAt: 0)
            
            let row = "\(String(index + 1).padding(toLength: 5, withPad: " ", startingAt: 0)) \(String(process.pid).padding(toLength: 8, withPad: " ", startingAt: 0)) \(paddedName) \(paddedMem) \(percentStr) \(String(process.threadCount).padding(toLength: 8, withPad: " ", startingAt: 0)) \(process.status)"
            
            print(colored(row, color: color))
        }
        print()
    }
    
    static func printMemoryBar(label: String, used: UInt64, total: UInt64, width: Int = 50) {
        let percentage = Double(used) / Double(total)
        let filledWidth = Int(percentage * Double(width))
        let emptyWidth = width - filledWidth
        
        let bar = String(repeating: "█", count: filledWidth) +
                 String(repeating: "░", count: emptyWidth)
        
        let color: Color = percentage > 0.8 ? .red :
                          percentage > 0.6 ? .yellow : .green
        
        let percentStr = String(format: "%.1f%%", percentage * 100)
        print("\(label): [\(colored(bar, color: color))] \(percentStr)")
    }
    
    static func printASCIIGraph(_ processes: [ProcessMemoryInfo], topN: Int = 10) {
        printHeader("TOP \(topN) PROCESSES - MEMORY USAGE")
        
        let displayProcesses = Array(processes.prefix(topN))
        guard let maxMemory = displayProcesses.first?.memoryBytes, maxMemory > 0 else { return }
        
        let barWidth = 60
        
        for process in displayProcesses {
            let percentage = Double(process.memoryBytes) / Double(maxMemory)
            let filledWidth = Int(percentage * Double(barWidth))
            let bar = String(repeating: "█", count: filledWidth)
            
            let color: Color = process.memoryPercent > 5.0 ? .red :
                              process.memoryPercent > 2.0 ? .yellow : .green
            
            let name = String(process.name.prefix(25)).padding(toLength: 25, withPad: " ", startingAt: 0)
            let memory = process.formattedMemory.padding(toLength: 12, withPad: " ", startingAt: 0)
            
            print("\(name) \(memory) [\(colored(bar, color: color))]")
        }
        print()
    }
    
    static func showProgress(current: Int, total: Int, label: String = "Processing") {
        let percentage = Double(current) / Double(total) * 100
        let barWidth = 50
        let filled = Int(Double(barWidth) * percentage / 100)
        let bar = String(repeating: "█", count: filled) + String(repeating: "░", count: barWidth - filled)
        
        print("\r\(label): [\(bar)] \(Int(percentage))% (\(current)/\(total))", terminator: "")
        fflush(stdout)
        
        if current >= total {
            print() // New line when complete
        }
    }
}
