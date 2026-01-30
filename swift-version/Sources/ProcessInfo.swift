import Foundation
import Darwin

struct ProcessMemoryInfo {
    let pid: Int32
    let name: String
    let memoryBytes: UInt64
    let memoryPercent: Double
    let threadCount: Int
    let status: String
    
    var formattedMemory: String {
        ByteFormatter.format(bytes: memoryBytes)
    }
}

struct SystemMemoryInfo {
    let totalMemory: UInt64
    let usedMemory: UInt64
    let freeMemory: UInt64
    let availableMemory: UInt64
    let wiredMemory: UInt64
    
    var percentUsed: Double {
        return Double(usedMemory) / Double(totalMemory) * 100
    }
    
    var formattedTotal: String { ByteFormatter.format(bytes: totalMemory) }
    var formattedUsed: String { ByteFormatter.format(bytes: usedMemory) }
    var formattedFree: String { ByteFormatter.format(bytes: freeMemory) }
    var formattedAvailable: String { ByteFormatter.format(bytes: availableMemory) }
}

class ProcessMonitor {
    func getSystemMemoryInfo() -> SystemMemoryInfo? {
        var vmStats = vm_statistics64()
        var count = mach_msg_type_number_t(MemoryLayout<vm_statistics64>.size / MemoryLayout<integer_t>.size)
        
        let result = withUnsafeMutablePointer(to: &vmStats) {
            $0.withMemoryRebound(to: integer_t.self, capacity: Int(count)) {
                host_statistics64(mach_host_self(), HOST_VM_INFO64, $0, &count)
            }
        }
        
        guard result == KERN_SUCCESS else { return nil }
        
        let pageSize = UInt64(sysconf(_SC_PAGESIZE))
        let totalMemory = ProcessInfo.processInfo.physicalMemory
        let freeMemory = UInt64(vmStats.free_count) * pageSize
        let activeMemory = UInt64(vmStats.active_count) * pageSize
        let inactiveMemory = UInt64(vmStats.inactive_count) * pageSize
        let wiredMemory = UInt64(vmStats.wire_count) * pageSize
        let compressedMemory = UInt64(vmStats.compressor_page_count) * pageSize
        
        let usedMemory = activeMemory + inactiveMemory + wiredMemory + compressedMemory
        let availableMemory = totalMemory - usedMemory
        
        return SystemMemoryInfo(
            totalMemory: totalMemory,
            usedMemory: usedMemory,
            freeMemory: freeMemory,
            availableMemory: availableMemory,
            wiredMemory: wiredMemory
        )
    }
    
    func getAllProcesses() -> [ProcessMemoryInfo] {
        var processes: [ProcessMemoryInfo] = []
        var processCount: pid_t = 0
        
        // Get process count
        var result = proc_listallpids(nil, 0)
        guard result > 0 else { return processes }
        
        processCount = result
        var pids = [pid_t](repeating: 0, count: Int(processCount))
        
        // Get all PIDs
        result = proc_listallpids(&pids, Int32(MemoryLayout<pid_t>.size * Int(processCount)))
        guard result > 0 else { return processes }
        
        let systemMemory = getSystemMemoryInfo()
        let totalMemory = Double(systemMemory?.totalMemory ?? 1)
        
        for pid in pids where pid > 0 {
            if let processInfo = getProcessInfo(pid: pid, totalMemory: totalMemory) {
                processes.append(processInfo)
            }
        }
        
        return processes.sorted { $0.memoryBytes > $1.memoryBytes }
    }
    
    private func getProcessInfo(pid: pid_t, totalMemory: Double) -> ProcessMemoryInfo? {
        var taskInfo = task_vm_info_data_t()
        var count = mach_msg_type_number_t(MemoryLayout<task_vm_info_data_t>.size / MemoryLayout<natural_t>.size)
        
        var task: task_t = 0
        var result = task_for_pid(mach_task_self_, pid, &task)
        
        guard result == KERN_SUCCESS else { return nil }
        
        result = withUnsafeMutablePointer(to: &taskInfo) {
            $0.withMemoryRebound(to: integer_t.self, capacity: Int(count)) {
                task_info(task, task_flavor_t(TASK_VM_INFO), $0, &count)
            }
        }
        
        guard result == KERN_SUCCESS else { return nil }
        
        let memoryBytes = UInt64(taskInfo.phys_footprint)
        let memoryPercent = (Double(memoryBytes) / totalMemory) * 100
        
        // Get process name
        let pathMaxSize = 4096
        var pathBuffer = [CChar](repeating: 0, count: pathMaxSize)
        proc_pidpath(pid, &pathBuffer, UInt32(pathMaxSize))
        
        let fullPath = String(cString: pathBuffer)
        let processName = (fullPath as NSString).lastPathComponent
        
        // Get thread count
        var threadList: thread_act_array_t?
        var threadCount: mach_msg_type_number_t = 0
        let threadResult = task_threads(task, &threadList, &threadCount)
        
        let threads = threadResult == KERN_SUCCESS ? Int(threadCount) : 0
        
        // Clean up thread list
        if let list = threadList {
            vm_deallocate(mach_task_self_, vm_address_t(bitPattern: list), vm_size_t(threadCount) * vm_size_t(MemoryLayout<thread_t>.size))
        }
        
        return ProcessMemoryInfo(
            pid: pid,
            name: processName.isEmpty ? "Unknown" : processName,
            memoryBytes: memoryBytes,
            memoryPercent: memoryPercent,
            threadCount: threads,
            status: "running"
        )
    }
}

struct ByteFormatter {
    static func format(bytes: UInt64) -> String {
        let units = ["B", "KB", "MB", "GB", "TB"]
        var value = Double(bytes)
        var unitIndex = 0
        
        while value >= 1024 && unitIndex < units.count - 1 {
            value /= 1024
            unitIndex += 1
        }
        
        return String(format: "%.2f %@", value, units[unitIndex])
    }
}
