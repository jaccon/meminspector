#!/usr/bin/env python3
"""
MemInspector - Memory Inspector for macOS
Tool to analyze memory consumption of applications and threads on macOS
"""

import psutil
import sys
from tqdm import tqdm
from collections import defaultdict
import time
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import BarColumn, Progress, TextColumn
from rich.text import Text
from rich import box
import threading
import queue
import select
import tty
import termios

# Try to import docker
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False


class MemInspector:
    def __init__(self):
        self.processes = []
        self.history_timestamps = []
        self.history_memory_used = []
        self.history_memory_available = []
        self.history_top_processes = defaultdict(list)
        self.console = Console()
        self.show_graph = False
        self.stop_tui = False
        self.docker_client = None
        self.docker_error = None
        
        # Try to connect to Docker
        if DOCKER_AVAILABLE:
            try:
                self.docker_client = docker.from_env()
                # Test connection
                self.docker_client.ping()
            except docker.errors.DockerException as e:
                self.docker_error = f"Docker connection error: {str(e)}"
                self.docker_client = None
            except Exception as e:
                self.docker_error = f"Unexpected error: {str(e)}"
                self.docker_client = None
        else:
            self.docker_error = "Docker library not installed (pip install docker)"
        
    def format_bytes(self, bytes_value):
        """Converts bytes to readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def get_process_info(self, proc):
        """Gets information from a process"""
        try:
            pinfo = proc.as_dict(attrs=[
                'pid', 'name', 'memory_info', 'memory_percent',
                'num_threads', 'status', 'username'
            ])
            return pinfo
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    def get_thread_info(self, proc):
        """Gets thread information from a process"""
        try:
            threads = proc.threads()
            thread_info = []
            for thread in threads:
                thread_info.append({
                    'id': thread.id,
                    'user_time': thread.user_time,
                    'system_time': thread.system_time
                })
            return thread_info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
    def collect_processes(self):
        """Collects information from all processes"""
        print("\nCollecting process information...\n")
        
        all_processes = list(psutil.process_iter())
        
        for proc in tqdm(all_processes, desc="Analyzing processes", unit="proc"):
            pinfo = self.get_process_info(proc)
            if pinfo:
                self.processes.append(pinfo)
            time.sleep(0.001)  # Pequeno delay para não sobrecarregar o sistema
        
        # Ordena por uso de memória (RSS)
        self.processes.sort(
            key=lambda x: x['memory_info'].rss if x['memory_info'] else 0,
            reverse=True
        )
    
    def display_top_processes(self, top_n=None):
        """Displays processes that consume the most memory"""
        processes_to_show = self.processes if top_n is None else self.processes[:top_n]
        count = len(processes_to_show)
        
        print(f"\n{'='*100}")
        print(f"ALL PROCESSES BY MEMORY USAGE ({count} processes)")
        print(f"{'='*100}\n")
        
        print(f"{'#':<4} {'PID':<8} {'Name':<30} {'Memory RSS':<15} {'% Mem':<8} {'Threads':<8} {'Status':<12}")
        print(f"{'-'*100}")
        
        for idx, proc in enumerate(processes_to_show, 1):
            pid = proc.get('pid', 'N/A')
            name = proc.get('name', 'N/A')[:29]
            mem_info = proc.get('memory_info')
            rss = self.format_bytes(mem_info.rss) if mem_info else 'N/A'
            mem_pct = proc.get('memory_percent', 0)
            mem_percent = f"{mem_pct:.2f}%" if mem_pct is not None else "0.00%"
            num_threads = proc.get('num_threads', 0)
            status = proc.get('status', 'N/A')
            
            print(f"{idx:<4} {pid:<8} {name:<30} {rss:<15} {mem_percent:<8} {num_threads:<8} {status:<12}")
    
    def analyze_threads(self, top_n=5):
        """Analyzes threads from processes that consume the most memory"""
        print(f"\n{'='*100}")
        print(f"THREAD ANALYSIS OF TOP {top_n} PROCESSES")
        print(f"{'='*100}\n")
        
        processes_to_analyze = self.processes[:top_n]
        
        for proc_info in tqdm(processes_to_analyze, desc="Analyzing threads", unit="proc"):
            try:
                proc = psutil.Process(proc_info['pid'])
                threads = self.get_thread_info(proc)
                
                print(f"\nProcess: {proc_info['name']} (PID: {proc_info['pid']})")
                print(f"   Memory RSS: {self.format_bytes(proc_info['memory_info'].rss)}")
                print(f"   Total Threads: {len(threads)}")
                
                if threads:
                    # Sort threads by CPU time (user_time + system_time)
                    threads_sorted = sorted(
                        threads,
                        key=lambda t: t['user_time'] + t['system_time'],
                        reverse=True
                    )
                    
                    print(f"\n   {'Thread ID':<15} {'User Time':<15} {'System Time':<15} {'Total Time':<15}")
                    print(f"   {'-'*60}")
                    
                    for thread in threads_sorted[:5]:  # Top 5 threads
                        total_time = thread['user_time'] + thread['system_time']
                        print(f"   {thread['id']:<15} {thread['user_time']:<15.2f} {thread['system_time']:<15.2f} {total_time:<15.2f}")
                
                time.sleep(0.001)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"   Unable to access process information")
    
    def display_system_summary(self):
        """Displays system summary"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        print(f"\n{'='*100}")
        print("SYSTEM SUMMARY")
        print(f"{'='*100}\n")
        
        print(f"Total Memory:      {self.format_bytes(memory.total)}")
        print(f"Available Memory:  {self.format_bytes(memory.available)}")
        print(f"Used Memory:       {self.format_bytes(memory.used)} ({memory.percent}%)")
        print(f"Free Memory:       {self.format_bytes(memory.free)}")
        
        print(f"\nTotal Swap:        {self.format_bytes(swap.total)}")
        print(f"Used Swap:         {self.format_bytes(swap.used)} ({swap.percent}%)")
        print(f"Free Swap:         {self.format_bytes(swap.free)}")
        
        print(f"\nTotal Processes:   {len(self.processes)}")
        
        # Docker summary
        if self.docker_client:
            containers = self.get_docker_containers()
            if containers:
                print(f"\n{'='*100}")
                print(f"DOCKER CONTAINERS ({len(containers)} running)")
                print(f"{'='*100}\n")
                print(f"{'#':<4} {'Name':<30} {'Image':<35} {'Memory':<15} {'%':<8}")
                print(f"{'-'*100}")
                
                for idx, container in enumerate(containers, 1):
                    mem_usage = self.format_bytes(container['memory_usage'])
                    mem_percent = f"{container['memory_percent']:.1f}%"
                    print(
                        f"{idx:<4} "
                        f"{container['name'][:29]:<30} "
                        f"{container['image'][:34]:<35} "
                        f"{mem_usage:<15} "
                        f"{mem_percent:<8}"
                    )
    
    def run(self, top_processes=None, analyze_threads_count=5):
        """Executes the complete analysis"""
        print("="*100)
        print("MemInspector - Memory Inspector for macOS")
        print("="*100)
        
        # System summary
        self.display_system_summary()
        
        # Collect processes
        self.collect_processes()
        
        # Display all processes
        self.display_top_processes(top_n=top_processes)
        
        # Analyze threads
        self.analyze_threads(top_n=analyze_threads_count)
        
        print(f"\n{'='*100}")
        print("Analysis completed!")
        print(f"{'='*100}\n")
    
    def update_graph(self, frame, fig, ax1, ax2, top_n=10, max_points=60):
        """Updates the real-time graph"""
        # Clear axes
        ax1.clear()
        ax2.clear()
        
        # Collect current data
        memory = psutil.virtual_memory()
        
        # Update history
        current_time = datetime.now().strftime('%H:%M:%S')
        self.history_timestamps.append(current_time)
        self.history_memory_used.append(memory.used / (1024**3))  # Convert to GB
        self.history_memory_available.append(memory.available / (1024**3))
        
        # Keep only last max_points
        if len(self.history_timestamps) > max_points:
            self.history_timestamps = self.history_timestamps[-max_points:]
            self.history_memory_used = self.history_memory_used[-max_points:]
            self.history_memory_available = self.history_memory_available[-max_points:]
        
        # Get top processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                pinfo = proc.info
                if pinfo['memory_info']:
                    processes.append({
                        'name': pinfo['name'],
                        'memory': pinfo['memory_info'].rss / (1024**3)  # GB
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        processes.sort(key=lambda x: x['memory'], reverse=True)
        top_processes = processes[:top_n]
        
        # Update top processes history
        for proc in top_processes:
            self.history_top_processes[proc['name']].append(proc['memory'])
        
        # Keep history aligned
        for name in list(self.history_top_processes.keys()):
            if len(self.history_top_processes[name]) > max_points:
                self.history_top_processes[name] = self.history_top_processes[name][-max_points:]
        
        # Plot 1: Total Memory Usage Over Time
        ax1.plot(self.history_timestamps, self.history_memory_used, 
                label='Used Memory', color='#e74c3c', linewidth=2)
        ax1.plot(self.history_timestamps, self.history_memory_available, 
                label='Available Memory', color='#2ecc71', linewidth=2)
        ax1.fill_between(range(len(self.history_memory_used)), 
                         self.history_memory_used, alpha=0.3, color='#e74c3c')
        
        ax1.set_title('System Memory Usage Over Time', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Time', fontsize=10)
        ax1.set_ylabel('Memory (GB)', fontsize=10)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Rotate x labels
        if len(self.history_timestamps) > 10:
            step = len(self.history_timestamps) // 10
            ax1.set_xticks(range(0, len(self.history_timestamps), step))
            ax1.set_xticklabels(self.history_timestamps[::step], rotation=45, ha='right')
        else:
            ax1.set_xticks(range(len(self.history_timestamps)))
            ax1.set_xticklabels(self.history_timestamps, rotation=45, ha='right')
        
        # Add current stats
        total_gb = memory.total / (1024**3)
        used_gb = memory.used / (1024**3)
        percent = memory.percent
        ax1.text(0.02, 0.98, f'Total: {total_gb:.2f} GB\nUsed: {used_gb:.2f} GB ({percent:.1f}%)',
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=9)
        
        # Plot 2: Top Processes Memory Usage
        process_names = [p['name'][:20] for p in top_processes]  # Truncate names
        process_memory = [p['memory'] for p in top_processes]
        
        colors = plt.cm.viridis(range(len(process_names)))
        bars = ax2.barh(process_names, process_memory, color=colors)
        
        ax2.set_title(f'Top {top_n} Processes by Memory Usage', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Memory (GB)', fontsize=10)
        ax2.set_ylabel('Process', fontsize=10)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, (bar, mem) in enumerate(zip(bars, process_memory)):
            ax2.text(mem, bar.get_y() + bar.get_height()/2, 
                    f' {mem:.3f} GB', 
                    va='center', fontsize=8)
        
        # Invert y-axis so highest is on top
        ax2.invert_yaxis()
        
        plt.tight_layout()
    
    def run_realtime_graph(self, top_n=10, update_interval=2000):
        """Runs real-time graph visualization"""
        print("="*100)
        print("MemInspector - Real-Time Memory Monitor")
        print("="*100)
        print(f"\nStarting real-time monitoring...")
        print(f"Showing top {top_n} processes")
        print(f"Update interval: {update_interval/1000:.1f} seconds")
        print("\nClose the graph window to exit.\n")
        
        # Create figure with 2 subplots
        fig = plt.figure(figsize=(14, 10))
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Create animation
        ani = animation.FuncAnimation(
            fig, 
            self.update_graph,
            fargs=(fig, ax1, ax2, top_n),
            interval=update_interval,
            cache_frame_data=False
        )
        
        plt.show()
    
    def run_refresh_mode(self, top_n=20, interval=3):
        """Runs continuous refresh mode in terminal"""
        print("="*100)
        print("MemInspector - Continuous Refresh Mode")
        print("="*100)
        print(f"\nRefresh interval: {interval} seconds")
        print(f"Showing top {top_n} processes")
        print("\nPress Ctrl+C to exit.\n")
        
        try:
            iteration = 0
            while True:
                iteration += 1
                
                # Clear screen (works on Unix-like systems)
                print("\033[2J\033[H", end="")
                
                # Show iteration info
                print("="*100)
                print(f"MemInspector - Continuous Refresh Mode (Update #{iteration})")
                print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*100)
                
                # Display system summary
                self.display_system_summary()
                
                # Collect and display processes
                self.processes = []
                all_processes = list(psutil.process_iter())
                
                for proc in all_processes:
                    pinfo = self.get_process_info(proc)
                    if pinfo:
                        self.processes.append(pinfo)
                
                # Sort by memory usage
                self.processes.sort(
                    key=lambda x: x['memory_info'].rss if x['memory_info'] else 0,
                    reverse=True
                )
                
                # Display top processes
                self.display_top_processes(top_n=top_n)
                
                print(f"\n{'='*100}")
                print(f"Next update in {interval} seconds... (Press Ctrl+C to exit)")
                print(f"{'='*100}")
                
                # Wait for next refresh
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nRefresh mode stopped by user.")
    
    def create_memory_bar(self, used, total, width=50):
        """Creates a colored memory usage bar"""
        percent = (used / total) * 100
        filled = int((used / total) * width)
        
        # Color based on usage
        if percent < 50:
            color = "green"
        elif percent < 75:
            color = "yellow"
        else:
            color = "red"
        
        bar = "█" * filled + "░" * (width - filled)
        return f"[{color}]{bar}[/{color}]"
    
    def create_system_panel(self):
        """Creates a panel with system memory information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Create table for system info
        table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        table.add_column("Label", style="cyan bold")
        table.add_column("Value", style="white")
        table.add_column("Bar", style="white")
        
        # Memory info
        mem_bar = self.create_memory_bar(memory.used, memory.total)
        table.add_row(
            "Total Memory",
            f"{self.format_bytes(memory.total)}",
            ""
        )
        table.add_row(
            "Used Memory",
            f"{self.format_bytes(memory.used)} ({memory.percent}%)",
            mem_bar
        )
        table.add_row(
            "Available",
            f"{self.format_bytes(memory.available)}",
            ""
        )
        
        # Swap info
        if swap.total > 0:
            swap_bar = self.create_memory_bar(swap.used, swap.total)
            table.add_row("", "", "")  # Spacer
            table.add_row(
                "Total Swap",
                f"{self.format_bytes(swap.total)}",
                ""
            )
            table.add_row(
                "Used Swap",
                f"{self.format_bytes(swap.used)} ({swap.percent}%)",
                swap_bar
            )
        
        return Panel(
            table,
            title="[bold cyan]System Memory[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def create_processes_table(self, top_n=20):
        """Creates a colored table with top processes"""
        # Collect current processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent', 'num_threads', 'status']):
            try:
                pinfo = proc.info
                if pinfo['memory_info']:
                    processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by memory
        processes.sort(key=lambda x: x['memory_info'].rss if x['memory_info'] else 0, reverse=True)
        top_processes = processes[:top_n]
        
        # Create table
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            title=f"[bold yellow]Top {top_n} Processes by Memory Usage[/bold yellow]",
            title_style="bold yellow"
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("PID", style="cyan", width=8)
        table.add_column("Name", style="green", width=30)
        table.add_column("Memory", style="yellow", width=15)
        table.add_column("%", style="magenta", width=8)
        table.add_column("Threads", style="blue", width=8)
        table.add_column("Status", style="white", width=10)
        
        # Add rows
        for idx, proc in enumerate(top_processes, 1):
            pid = str(proc.get('pid', 'N/A'))
            name = proc.get('name', 'N/A')[:29]
            mem_info = proc.get('memory_info')
            rss = self.format_bytes(mem_info.rss) if mem_info else 'N/A'
            mem_pct = proc.get('memory_percent', 0)
            mem_percent = f"{mem_pct:.2f}%" if mem_pct is not None else "0.00%"
            num_threads = str(proc.get('num_threads', 0))
            status = proc.get('status', 'N/A')
            
            # Color code based on memory percentage
            if mem_pct and mem_pct > 5:
                mem_style = "bold red"
            elif mem_pct and mem_pct > 2:
                mem_style = "bold yellow"
            else:
                mem_style = "white"
            
            table.add_row(
                str(idx),
                pid,
                name,
                f"[{mem_style}]{rss}[/{mem_style}]",
                f"[{mem_style}]{mem_percent}[/{mem_style}]",
                num_threads,
                status
            )
        
        return table
    
    def create_memory_graph_ascii(self, width=60, height=10):
        """Creates an ASCII graph of memory usage"""
        memory = psutil.virtual_memory()
        
        # Get historical data or use current
        if len(self.history_memory_used) < 2:
            # Not enough data yet
            return Text("Collecting data...", style="yellow")
        
        # Use last 'width' points
        data_points = self.history_memory_used[-width:]
        max_mem = max(data_points) if data_points else 1
        
        # Create graph
        lines = []
        for h in range(height, 0, -1):
            line = ""
            threshold = (h / height) * max_mem
            for point in data_points:
                if point >= threshold:
                    line += "█"
                else:
                    line += " "
            
            # Color based on height
            if h > height * 0.7:
                lines.append(f"[red]{line}[/red]")
            elif h > height * 0.4:
                lines.append(f"[yellow]{line}[/yellow]")
            else:
                lines.append(f"[green]{line}[/green]")
        
        graph_text = "\n".join(lines)
        return Text.from_markup(graph_text)
    
    def get_docker_containers(self):
        """Gets Docker containers and their memory usage"""
        if not self.docker_client:
            return []
        
        try:
            containers = []
            running_containers = self.docker_client.containers.list()
            
            # Debug: log number of containers found
            if len(running_containers) == 0:
                self.docker_error = "No running containers found"
                return []
            
            for container in running_containers:
                try:
                    # Get container stats (this can take time)
                    stats = container.stats(stream=False)
                    
                    # Calculate memory usage
                    memory_stats = stats.get('memory_stats', {})
                    
                    if not memory_stats:
                        # No memory stats available
                        continue
                    
                    memory_usage = memory_stats.get('usage', 0)
                    memory_limit = memory_stats.get('limit', 1)
                    
                    # Some systems report cache separately
                    cache = memory_stats.get('stats', {}).get('cache', 0)
                    if cache > 0 and memory_usage > cache:
                        memory_usage = memory_usage - cache
                    
                    memory_percent = (memory_usage / memory_limit * 100) if memory_limit > 0 else 0
                    
                    # Get image name
                    image_name = 'unknown'
                    try:
                        if container.image.tags:
                            image_name = container.image.tags[0]
                        else:
                            # Try to get from config
                            config_image = container.attrs.get('Config', {}).get('Image', '')
                            if config_image:
                                image_name = config_image.split(':')[0] if ':' in config_image else config_image
                    except:
                        image_name = 'unknown'
                    
                    containers.append({
                        'id': container.short_id,
                        'name': container.name,
                        'image': image_name,
                        'status': container.status,
                        'memory_usage': memory_usage,
                        'memory_limit': memory_limit,
                        'memory_percent': memory_percent
                    })
                except Exception as e:
                    # Log error but continue with other containers
                    continue
            
            # Sort by memory usage
            containers.sort(key=lambda x: x['memory_usage'], reverse=True)
            
            # Clear error if we got containers successfully
            if containers:
                self.docker_error = None
            
            return containers
        except Exception as e:
            self.docker_error = f"Error listing containers: {str(e)}"
            return []
    
    def create_docker_table(self):
        """Creates a table with Docker containers"""
        if not DOCKER_AVAILABLE:
            return Panel(
                "[yellow]Docker library not installed[/yellow]\n[dim]Install with: pip install docker[/dim]",
                title="[bold blue]Docker Containers[/bold blue]",
                border_style="blue",
                box=box.ROUNDED
            )
        
        if not self.docker_client:
            error_msg = self.docker_error or "Docker daemon not running"
            return Panel(
                f"[yellow]{error_msg}[/yellow]\n[dim]Make sure Docker Desktop is running[/dim]",
                title="[bold blue]Docker Containers[/bold blue]",
                border_style="blue",
                box=box.ROUNDED
            )
        
        containers = self.get_docker_containers()
        
        if not containers:
            msg = "[dim]No running containers[/dim]"
            if self.docker_error:
                msg = f"[yellow]{self.docker_error}[/yellow]"
            return Panel(
                msg,
                title="[bold blue]Docker Containers[/bold blue]",
                border_style="blue",
                box=box.ROUNDED
            )
        
        # Create table
        table = Table(
            show_header=True,
            header_style="bold blue",
            box=box.SIMPLE,
            padding=(0, 1),
            show_lines=False
        )
        
        table.add_column("#", style="dim", width=3)
        table.add_column("Name", style="green bold", width=18, no_wrap=False)
        table.add_column("Memory", style="magenta", width=12)
        table.add_column("%", style="red bold", width=7)
        
        # Add rows - show all containers or top 15
        display_count = min(len(containers), 15)
        for idx, container in enumerate(containers[:display_count], 1):
            mem_usage = self.format_bytes(container['memory_usage'])
            mem_percent = f"{container['memory_percent']:.1f}%"
            
            # Color code based on memory percentage
            if container['memory_percent'] > 80:
                mem_style = "bold red"
            elif container['memory_percent'] > 50:
                mem_style = "bold yellow"
            else:
                mem_style = "white"
            
            # Truncate name if needed
            name = container['name']
            if len(name) > 18:
                name = name[:15] + "..."
            
            table.add_row(
                str(idx),
                name,
                f"[{mem_style}]{mem_usage}[/{mem_style}]",
                f"[{mem_style}]{mem_percent}[/{mem_style}]"
            )
        
        title_text = f"[bold blue]Docker Containers ({len(containers)} running)[/bold blue]"
        return Panel(
            table,
            title=title_text,
            border_style="blue",
            box=box.ROUNDED
        )
    
    def run_colored_tui(self, top_n=20, interval=2):
        """Runs a colored terminal UI with live updates"""
        self.console.print("\n[bold cyan]MemInspector - Colored Terminal Interface[/bold cyan]")
        self.console.print("[dim]Press 'q' or 'ESC' to exit | Ctrl+C to force quit[/dim]\n")
        time.sleep(1)  # Give user time to read the message
        
        # Save terminal settings
        old_settings = None
        if sys.stdin.isatty():
            old_settings = termios.tcgetattr(sys.stdin)
        
        # Create a queue for keyboard input
        input_queue = queue.Queue()
        
        def keyboard_listener():
            """Thread to listen for keyboard input"""
            try:
                if sys.stdin.isatty():
                    tty.setcbreak(sys.stdin.fileno())
                
                while not self.stop_tui:
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        char = sys.stdin.read(1)
                        if char.lower() == 'q':
                            input_queue.put('quit')
                            break
                        elif char == '\x1b':  # ESC key
                            input_queue.put('quit')
                            break
            except Exception as e:
                pass
            finally:
                if old_settings and sys.stdin.isatty():
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
        # Start keyboard listener thread
        listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
        listener_thread.start()
        
        try:
            with Live(self.create_layout(top_n), refresh_per_second=1, console=self.console) as live:
                while not self.stop_tui:
                    # Check for keyboard input
                    try:
                        command = input_queue.get_nowait()
                        if command == 'quit':
                            self.stop_tui = True
                            break
                    except queue.Empty:
                        pass
                    
                    # Update history for graph
                    memory = psutil.virtual_memory()
                    self.history_memory_used.append(memory.used / (1024**3))
                    self.history_memory_available.append(memory.available / (1024**3))
                    
                    # Keep only last 60 points
                    if len(self.history_memory_used) > 60:
                        self.history_memory_used = self.history_memory_used[-60:]
                        self.history_memory_available = self.history_memory_available[-60:]
                    
                    # Update display
                    live.update(self.create_layout(top_n))
                    time.sleep(interval)
            
            self.console.print("\n[green]Application closed.[/green]")
                    
        except KeyboardInterrupt:
            self.stop_tui = True
            self.console.print("\n[yellow]Monitoring stopped by user.[/yellow]")
        finally:
            # Restore terminal settings
            if old_settings and sys.stdin.isatty():
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    def create_layout(self, top_n):
        """Creates the complete layout for the TUI"""
        layout = Layout()
        
        # Check if Docker is available to adjust layout
        has_docker = self.docker_client is not None
        
        if has_docker:
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="body"),
                Layout(name="footer", size=3),
            )
            
            layout["body"].split_row(
                Layout(name="left", ratio=3),
                Layout(name="right", ratio=2),
            )
            
            layout["left"].split_column(
                Layout(name="processes"),
                Layout(name="graph", size=12),
            )
            
            layout["right"].split_column(
                Layout(name="system"),
                Layout(name="docker"),
            )
        else:
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="body"),
                Layout(name="footer", size=3),
            )
            
            layout["body"].split_row(
                Layout(name="left", ratio=2),
                Layout(name="right", ratio=1),
            )
            
            layout["left"].split_column(
                Layout(name="processes"),
                Layout(name="graph", size=12),
            )
        
        # Header
        header_text = Text()
        header_text.append("MemInspector", style="bold cyan")
        header_text.append(" | ", style="dim")
        header_text.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style="bold white")
        header_text.append(" | ", style="dim")
        header_text.append(f"Total Processes: {len(list(psutil.process_iter()))}", style="green")
        if has_docker:
            containers_count = len(self.get_docker_containers())
            header_text.append(" | ", style="dim")
            header_text.append(f"Docker: {containers_count} containers", style="blue")
        header_text.append(" | ", style="dim")
        header_text.append("Press 'q' or 'ESC' to exit", style="yellow italic")
        
        layout["header"].update(Panel(header_text, border_style="blue"))
        
        # System info
        if has_docker:
            layout["system"].update(self.create_system_panel())
            layout["docker"].update(self.create_docker_table())
        else:
            layout["right"].update(self.create_system_panel())
        
        # Processes table
        layout["processes"].update(self.create_processes_table(top_n))
        
        # Memory graph
        graph = self.create_memory_graph_ascii()
        graph_panel = Panel(
            graph,
            title="[bold green]Memory Usage Trend[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        layout["graph"].update(graph_panel)
        
        # Footer
        footer_text = Text()
        footer_text.append("Developed by ", style="dim")
        footer_text.append("Jaccon", style="bold cyan")
        footer_text.append(" | ", style="dim")
        footer_text.append("github.com/jaccon/meminspector", style="blue italic")
        
        layout["footer"].update(Panel(footer_text, border_style="dim", box=box.ROUNDED))
        
        return layout


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='MemInspector - Memory Inspector for macOS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 meminspector.py              # List all processes (default)
  python3 meminspector.py --list       # List all processes
  python3 meminspector.py --tui        # Colored terminal interface (recommended)
  python3 meminspector.py --graph      # Show real-time graphs
  python3 meminspector.py -g -t 15     # Show graphs with top 15 processes
  python3 meminspector.py -g -i 1      # Update graphs every 1 second
  python3 meminspector.py --refresh    # Continuous refresh in terminal
  python3 meminspector.py -r -t 20 -i 5 # Refresh top 20 every 5 seconds
  python3 meminspector.py --tui -t 30  # TUI with top 30 processes
        """
    )
    
    parser.add_argument('-l', '--list', action='store_true',
                       help='List all processes by memory usage (default mode)')
    parser.add_argument('-g', '--graph', action='store_true',
                       help='Show real-time memory usage graphs')
    parser.add_argument('-r', '--refresh', action='store_true',
                       help='Continuous refresh mode in terminal')
    parser.add_argument('--tui', action='store_true',
                       help='Colored terminal user interface (recommended)')
    parser.add_argument('-t', '--top', type=int, default=10,
                       help='Number of top processes to show (default: 10 for graph/refresh, 20 for TUI, all for list)')
    parser.add_argument('-i', '--interval', type=float, default=2.0,
                       help='Update interval in seconds (default: 2.0)')
    parser.add_argument('-a', '--analyze', type=int, default=5,
                       help='Number of processes to analyze threads (list mode only, default: 5)')
    
    args = parser.parse_args()
    
    try:
        # Check if running on macOS
        if sys.platform != 'darwin':
            print("Warning: This application was designed for macOS.")
            response = input("Do you want to continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(0)
        
        inspector = MemInspector()
        
        # If TUI flag is set, run colored terminal interface
        if args.tui:
            top_count = args.top if args.top != 10 else 20  # Default to 20 for TUI
            inspector.run_colored_tui(
                top_n=top_count,
                interval=args.interval
            )
        # If graph flag is set, run real-time graph mode
        elif args.graph:
            inspector.run_realtime_graph(
                top_n=args.top,
                update_interval=int(args.interval * 1000)
            )
        # If refresh flag is set, run continuous refresh mode
        elif args.refresh:
            top_count = args.top if args.top != 10 else 20  # Default to 20 for refresh mode
            inspector.run_refresh_mode(
                top_n=top_count,
                interval=args.interval
            )
        else:
            # Default: list mode (single run)
            inspector.run(top_processes=None, analyze_threads_count=args.analyze)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
