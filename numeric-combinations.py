from typing import List, Set, Tuple
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.layout import Layout
from datetime import datetime
import argparse

console = Console()

def strikeout(text: str) -> str:
    return "".join(char + "\u0336" for char in text)

# Safe evaluation with limited builtins
def safe_eval(expr: str) -> float:
    try:
        return eval(expr, {"__builtins__": {}}, {})
    except Exception:
        return None

# Generate expressions using only +, -, *, /
def generate_expressions(digits: str) -> Set[str]:
    memo = {}

    def helper(start: int, end: int) -> List[str]:
        key = (start, end)
        if key in memo:
            return memo[key]

        results = []
        token = digits[start:end+1]
        results.append(token)

        for i in range(start, end):
            left_exprs = helper(start, i)
            right_exprs = helper(i + 1, end)

            for left in left_exprs:
                for right in right_exprs:
                    if right != "0":  # Avoid zero division
                        results.append(f"({left})+({right})")
                        results.append(f"({left})-({right})")
                        results.append(f"({left})*({right})")
                        results.append(f"({left})/({right})")

        memo[key] = results
        return results

    return set(helper(0, len(digits) - 1))

def find_matching_expressions(digits: str, target: float, tolerance: float = 1e-6) -> List[str]:
    all_exprs = generate_expressions(digits)
    matches = []
    total_attempts = len(all_exprs)
    
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    )
    task = progress.add_task(f"Evaluating expressions...", total=total_attempts)
    
    current_expr = Text("")
    expr_panel = Panel(current_expr, title="Current Expression", border_style="blue")
    
    # Create a layout to hold both progress and panel
    layout = Layout()
    layout.split_column(
        Layout(progress, name="progress"),
        Layout(expr_panel, name="expression")
    )
    
    with Live(layout, refresh_per_second=10, console=console) as live:
        for i, expr in enumerate(all_exprs, 1):
            value = safe_eval(expr)
            if value is not None:
                if abs(value - target) < tolerance:
                    matches.append(expr)
                    current_expr = Text(f"✓ Found match: {expr} = {value}", style="green")
                else:
                    current_expr = Text(strikeout(f"Attempt {i}/{total_attempts}: {expr} = {value}"), style="dim")
            else:
                current_expr = Text(strikeout(f"Attempt {i}/{total_attempts}: {expr} (invalid)"), style="dim")
            
            progress.update(task, advance=1)
            expr_panel.renderable = current_expr
            live.update(layout)
    
    return matches

def save_results(digits: str, target: float, matches: List[str], filename: str):
    with open(filename, 'w') as f:
        f.write(f"Results for digits '{digits}' targeting {target}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total matches found: {len(matches)}\n\n")
        for i, match in enumerate(matches, 1):
            f.write(f"{i}. {match}\n")

def main():
    parser = argparse.ArgumentParser(description='Find numeric expressions that equal a target value.')
    parser.add_argument('digits', type=str, nargs='?', default="987654321",
                       help='String of digits to use (default: "987654321")')
    parser.add_argument('target', type=float, nargs='?', default=100,
                       help='Target value to find expressions for (default: 100)')
    parser.add_argument('--tolerance', type=float, default=1e-6,
                       help='Tolerance for floating point comparison (default: 1e-6)')
    
    args = parser.parse_args()
    
    # Validate digits input
    if not args.digits.isdigit():
        console.print("[red]Error: digits must contain only numeric characters[/red]")
        return
    
    console.print(f"[bold]Finding expressions for {args.digits} that equal {args.target}[/bold]")
    matches = find_matching_expressions(args.digits, args.target, args.tolerance)
    
    # Save results to file
    filename = f"{args.digits}_{int(args.target)}.txt"
    save_results(args.digits, args.target, matches, filename)
    
    if matches:
        console.print(f"\n[bold green]Found {len(matches)} matching expressions:[/bold green]")
        for m in matches:
            console.print(f"[green]{m}[/green]")
        console.print(f"\n[bold blue]Results saved to: {filename}[/bold blue]")
    else:
        console.print("[red]No matching expressions found[/red]")
        console.print(f"\n[bold blue]Empty results saved to: {filename}[/bold blue]")

if __name__ == "__main__":
    main()