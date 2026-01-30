import Foundation

let args = parseArguments()
if args.showHelp {
    printHelp()
} else {
    switch args.mode {
    case .list: runListMode(topN: args.topN)
    case .tui: runTUIMode(topN: args.topN, interval: args.interval)
    case .refresh: runRefreshMode(topN: args.topN, interval: args.interval)
    case .graph: runGraphMode(topN: args.topN)
    }
}
