

#Simple Network Traffic Tracker
#Monitors network sent/received bytes over time using psutil

import psutil
import time
from datetime import datetime


def get_network_stats():
    """Get current network bytes sent/received"""
    stats = psutil.net_io_counters()
    return stats.bytes_sent, stats.bytes_recv


def format_bytes(bytes_val):
    """Convert bytes to human readable format"""
    units = ['B', 'KB', 'MB', 'GB']
    for unit in units:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} TB"


def calculate_rate(current, previous, time_diff):
    """Calculate data rate in bytes per second"""
    if time_diff <= 0:
        return 0
    return max(0, (current - previous) / time_diff)


def display_stats(sent_total, recv_total, sent_rate, recv_rate):
    """Display current network statistics"""
    print(f"\r{datetime.now().strftime('%H:%M:%S')} | "
          f"Sent: {format_bytes(sent_total)} ({format_bytes(sent_rate)}/s) | "
          f"Recv: {format_bytes(recv_total)} ({format_bytes(recv_rate)}/s)", 
          end="", flush=True)


def track_network_traffic(interval=1):
    """Main tracking function - monitors network traffic continuously"""
    print("Network Traffic Tracker (Functional)")
    print("====================================")
    print("Press Ctrl+C to stop")
    
    # Get initial readings
    prev_sent, prev_recv = get_network_stats()
    prev_time = time.time()
    
    try:
        while True:
            time.sleep(interval)
            
            # Get current readings
            curr_sent, curr_recv = get_network_stats()
            curr_time = time.time()
            time_diff = curr_time - prev_time
            
            # Calculate rates
            sent_rate = calculate_rate(curr_sent, prev_sent, time_diff)
            recv_rate = calculate_rate(curr_recv, prev_recv, time_diff)
            
            # Display stats
            display_stats(curr_sent, curr_recv, sent_rate, recv_rate)
            
            # Update previous values
            prev_sent, prev_recv, prev_time = curr_sent, curr_recv, curr_time
            
    except KeyboardInterrupt:
        print("\n\nTracking stopped.")
        final_sent, final_recv = get_network_stats()
        print(f"Final totals - Sent: {format_bytes(final_sent)}, "
              f"Received: {format_bytes(final_recv)}")


def show_current_stats():
    """Show a one-time snapshot of network statistics"""
    sent, recv = get_network_stats()
    print(f"Current Network Stats:")
    print(f"  Bytes Sent: {format_bytes(sent)}")
    print(f"  Bytes Received: {format_bytes(recv)}")
    print(f"  Total: {format_bytes(sent + recv)}")


def main():
    """Main function with simple menu"""
    print("Simple Network Traffic Tracker")
    print("1. Start continuous monitoring")
    print("2. Show current stats")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        track_network_traffic()
    elif choice == '2':
        show_current_stats()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("Error: psutil required. Install with: pip install psutil")
        exit(1)
    
    main()