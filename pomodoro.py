#!/usr/bin/env python3
"""
Simple Pomodoro Timer

A command-line Pomodoro timer with desktop notifications.
Default settings: 25 min work, 5 min short break, 15 min long break, 4 sessions before long break.
"""

import time
import argparse
import os
from datetime import datetime, timedelta

# Try to import notification libraries, but continue if they're not available
try:
    import plyer.notification
    NOTIFY_AVAILABLE = True
except ImportError:
    NOTIFY_AVAILABLE = False

# Define colors for terminal output
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(seconds):
    """Format seconds into mm:ss string."""
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

def show_notification(title, message):
    """Show a desktop notification."""
    if NOTIFY_AVAILABLE:
        try:
            plyer.notification.notify(
                title=title,
                message=message,
                app_name="Pomodoro Timer",
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")
    else:
        # Print a more visible notification if desktop notifications aren't available
        print(f"\n{'='*50}")
        print(f"{Colors.YELLOW}{title}: {message}{Colors.RESET}")
        print(f"{'='*50}\n")

def countdown(duration, label, color, update_interval=1):
    """Run a countdown timer with a nice terminal display."""
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration)
    remaining = duration
    
    try:
        while remaining > 0:
            clear_screen()
            
            # Calculate progress bar (50 characters wide)
            progress_width = 50
            filled_width = int(progress_width * (duration - remaining) / duration)
            bar = "█" * filled_width + "░" * (progress_width - filled_width)
            
            # Calculate estimated end time
            end_time_str = end_time.strftime("%H:%M:%S")
            
            # Print timer information
            print(f"\n{color}╔{'═' * 60}╗{Colors.RESET}")
            print(f"{color}║{' ' * 24}POMODORO TIMER{' ' * 23}║{Colors.RESET}")
            print(f"{color}╠{'═' * 60}╣{Colors.RESET}")
            print(f"{color}║ Current Session: {label:<42} ║{Colors.RESET}")
            print(f"{color}║ Time Remaining: {format_time(remaining):<42} ║{Colors.RESET}")
            print(f"{color}║ End Time:       {end_time_str:<42} ║{Colors.RESET}")
            print(f"{color}║ Progress:       {bar} ║{Colors.RESET}")
            print(f"{color}╚{'═' * 60}╝{Colors.RESET}")
            print("\nPress Ctrl+C to pause/quit")
            
            time.sleep(update_interval)
            remaining = max(0, int((end_time - datetime.now()).total_seconds()))
            
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.YELLOW}Timer paused at {format_time(remaining)}{Colors.RESET}")
        
        while True:
            choice = input("\n[r]esume, [s]kip to next session, or [q]uit? ").lower()
            if choice == 'r':
                # Adjust end time based on the pause
                end_time = datetime.now() + timedelta(seconds=remaining)
                return countdown(remaining, label, color, update_interval)
            elif choice == 's':
                return True
            elif choice == 'q':
                raise SystemExit(0)
    
    # Timer completed normally
    return True

def run_pomodoro(work_time, short_break, long_break, sessions, auto_start):
    """Run the full Pomodoro sequence."""
    session_count = 1
    
    while True:
        # Work session
        print(f"\n{Colors.GREEN}Starting work session {session_count}/{sessions}{Colors.RESET}")
        if not auto_start:
            input("Press Enter to start...")
        
        show_notification("Pomodoro Timer", f"Starting work session {session_count}")
        countdown(work_time * 60, f"Work Session {session_count}/{sessions}", Colors.RED)
        show_notification("Pomodoro Timer", "Work session completed! Time for a break.")
        
        # Break session
        if session_count % sessions == 0:
            # Long break
            print(f"\n{Colors.GREEN}Time for a long break!{Colors.RESET}")
            if not auto_start:
                input("Press Enter to start long break...")
            
            show_notification("Pomodoro Timer", "Starting long break")
            countdown(long_break * 60, "Long Break", Colors.BLUE)
            show_notification("Pomodoro Timer", "Break completed! Ready for the next round?")
            
            choice = input(f"\n{Colors.YELLOW}Continue with another round? (y/n): {Colors.RESET}").lower()
            if choice != 'y':
                break
                
            session_count = 1
        else:
            # Short break
            print(f"\n{Colors.GREEN}Time for a short break!{Colors.RESET}")
            if not auto_start:
                input("Press Enter to start short break...")
            
            show_notification("Pomodoro Timer", "Starting short break")
            countdown(short_break * 60, "Short Break", Colors.GREEN)
            show_notification("Pomodoro Timer", "Break completed! Ready to work again?")
            session_count += 1

def main():
    """Parse command-line arguments and run the timer."""
    parser = argparse.ArgumentParser(description="Pomodoro Timer")
    parser.add_argument("--work", type=int, default=25, help="Work session duration in minutes (default: 25)")
    parser.add_argument("--short", type=int, default=5, help="Short break duration in minutes (default: 5)")
    parser.add_argument("--long", type=int, default=15, help="Long break duration in minutes (default: 15)")
    parser.add_argument("--sessions", type=int, default=4, help="Number of work sessions before a long break (default: 4)")
    parser.add_argument("--auto", action="store_true", help="Auto-start each session without prompting")
    args = parser.parse_args()
    
    try:
        clear_screen()
        print(f"\n{Colors.CYAN}Welcome to Pomodoro Timer!{Colors.RESET}")
        print(f"""
Settings:
- Work session: {args.work} minutes
- Short break: {args.short} minutes
- Long break: {args.long} minutes
- Sessions before long break: {args.sessions}
- Auto-start: {'Yes' if args.auto else 'No'}
""")
        
        if not NOTIFY_AVAILABLE:
            print(f"{Colors.YELLOW}Warning: Desktop notifications not available.{Colors.RESET}")
            print("To enable notifications, install the plyer package with: pip install plyer\n")
        
        input("Press Enter to start Pomodoro Timer...")
        run_pomodoro(args.work, args.short, args.long, args.sessions, args.auto)
        
        clear_screen()
        print(f"\n{Colors.PURPLE}Pomodoro Timer completed. Great job!{Colors.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Pomodoro Timer exited.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}\n")
    
if __name__ == "__main__":
    main()