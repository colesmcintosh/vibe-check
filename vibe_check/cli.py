#!/usr/bin/env python3
"""
Vibe Check - A professional CLI tool for security analysis using Claude 4
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

import click
import anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()


class SecurityAnalyzer:
    """Security analysis service using Claude 4"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def validate_api_connection(self) -> bool:
        """Validate that the API connection is working"""
        try:
            # Simple test to validate the connection
            self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=10,
                temperature=0.1,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except anthropic.APIError:
            return False

    def analyze_file(self, file_path: Path) -> str:
        """Analyze a code file for security vulnerabilities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    file_content = file.read()
            except OSError as exc:
                raise click.ClickException(f"Error reading file: {exc}") from exc
        except OSError as exc:
            raise click.ClickException(f"Error reading file: {exc}") from exc

        if not file_content.strip():
            raise click.ClickException(
                "File is empty or contains only whitespace"
            )

        prompt = self._create_security_prompt(file_path.name, file_content)

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.1,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.content[0].text
        except anthropic.APIError as exc:
            raise click.ClickException(
                f"Error communicating with Claude API: {exc}"
            ) from exc

    def _create_security_prompt(self, filename: str, code: str) -> str:
        """Create a comprehensive security analysis prompt"""
        return f"""You are a senior security engineer conducting a thorough \
security analysis. Please analyze the following code file for security \
vulnerabilities, best practices violations, and potential risks.

**File:** {filename}

**Code to analyze:**
```
{code}
```

Please provide a comprehensive security analysis in markdown format that includes:

## Executive Summary
- Brief overview of the security posture
- Risk level assessment (Low/Medium/High/Critical)
- Number of issues found by severity

## Security Findings

### Critical Issues
- List any critical security vulnerabilities that could lead to immediate compromise

### High Priority Issues
- Important security issues that should be addressed soon

### Medium Priority Issues
- Security concerns that should be addressed in the next development cycle

### Low Priority Issues
- Minor security improvements and best practices

## Detailed Analysis

For each finding, provide:
- **Issue**: Clear description of the problem
- **Location**: Line numbers or code sections where applicable
- **Risk**: Potential impact and likelihood
- **Recommendation**: Specific steps to fix the issue
- **Code Example**: Show how to fix it when applicable

## Security Best Practices
- Recommendations for improving overall security posture
- Preventive measures for similar issues

## Compliance & Standards
- Alignment with security standards (OWASP, CWE, etc.)
- Regulatory compliance considerations if applicable

## Conclusion
- Summary of key actions needed
- Prioritized remediation roadmap

Please be thorough but practical in your analysis. Focus on actionable \
recommendations that developers can implement."""


def load_api_key() -> str:
    """Load Anthropic API key from environment or prompt user"""
    # Try .env file first
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('ANTHROPIC_API_KEY='):
                    value = line.split('=', 1)[1].strip()
                    # Remove quotes if present (both single and double quotes)
                    if ((value.startswith('"') and value.endswith('"')) or
                            (value.startswith("'") and value.endswith("'"))):
                        value = value[1:-1]
                    return value

    # Try environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        return api_key

    # Prompt user for API key if not found
    console.print("\n[yellow]⚠️  Anthropic API key not found![/yellow]")
    console.print(
        "You need an API key to use Vibe Check. "
        "Get one at: https://console.anthropic.com/"
    )

    api_key = click.prompt(
        "\nPlease enter your Anthropic API key",
        type=str,
        hide_input=True,
        confirmation_prompt=False
    ).strip()

    if not api_key:
        raise click.ClickException("API key cannot be empty")

    # Validate API key format (basic check)
    if not api_key.startswith('sk-'):
        console.print(
            "[yellow]⚠️  Warning: API key doesn't start with 'sk-'. "
            "This might be incorrect.[/yellow]"
        )
        if not click.confirm("Continue anyway?"):
            raise click.Abort()

    # Ask user if they want to save the key
    save_key = click.confirm(
        "\nWould you like to save this API key to a .env file for future use?",
        default=True
    )

    if save_key:
        try:
            with open('.env', 'w', encoding='utf-8') as file:
                file.write("# Anthropic API Configuration\n")
                file.write(f"ANTHROPIC_API_KEY={api_key}\n")
            console.print("✅ [green]API key saved to .env file[/green]")
        except OSError as exc:
            console.print(
                f"[yellow]⚠️  Warning: Could not save API key to .env file: "
                f"{exc}[/yellow]"
            )
            console.print(
                "You may need to set the ANTHROPIC_API_KEY environment "
                "variable manually."
            )
    else:
        console.print(
            "[dim]Note: You'll need to enter your API key each time you "
            "run the tool.[/dim]"
        )

    return api_key


def validate_file_path(file_path: str) -> Path:
    """Validate and return Path object for the input file"""
    path = Path(file_path)

    if not path.exists():
        raise click.ClickException(f"File not found: {file_path}")

    if not path.is_file():
        raise click.ClickException(f"Path is not a file: {file_path}")

    # Check if it's a reasonable code file
    code_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h',
        '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt',
        '.scala', '.sh', '.bash', '.zsh', '.sql', '.html', '.css', '.scss',
        '.less', '.vue', '.svelte', '.dart', '.r', '.m', '.mm', '.pl',
        '.lua', '.nim', '.zig'
    }

    if path.suffix.lower() not in code_extensions:
        if not click.confirm(
            f"'{path.suffix}' is not a recognized code file extension. "
            "Continue anyway?"
        ):
            raise click.Abort()

    return path


def generate_report_filename(input_path: Path) -> Path:
    """Generate the output report filename in security_reports folder"""
    # Create security_reports directory if it doesn't exist
    reports_dir = Path("security_reports")
    reports_dir.mkdir(exist_ok=True)

    # Generate filename and return full path
    filename = f"{input_path.stem}_security_report.md"
    return reports_dir / filename


def write_report(output_path: Path, input_path: Path, analysis_result: str,
                 start_time: float, end_time: float) -> None:
    """Write the security analysis report to file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("# Security Analysis Report\n\n")
            file.write(f"**File Analyzed:** `{input_path}`\n")
            file.write(
                f"**Analysis Date:** "
                f"{time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            file.write(
                f"**Analysis Duration:** "
                f"{end_time - start_time:.2f} seconds\n"
            )
            file.write("**Tool:** Vibe Check\n\n")
            file.write("---\n\n")
            file.write(analysis_result)
    except OSError as exc:
        raise click.ClickException(f"Error writing report: {exc}") from exc


def perform_analysis(analyzer: SecurityAnalyzer, input_path: Path) -> tuple[str, float, float]:
    """Perform the security analysis with progress indicator"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(
            "🔎 Analyzing code for security vulnerabilities...",
            total=None
        )

        start_time = time.time()
        analysis_result = analyzer.analyze_file(input_path)
        end_time = time.time()

    return analysis_result, start_time, end_time


@click.command()
@click.argument('file_path', type=str, required=False)
@click.option(
    '--output', '-o',
    type=str,
    help='Custom output file path (default: {filename}_security_report.md)'
)
@click.option(
    '--api-key',
    type=str,
    help='Anthropic API key (can also be set via ANTHROPIC_API_KEY env var)'
)
@click.option(
    '--setup-key', '--setup',
    is_flag=True,
    help='Setup or update your Anthropic API key'
)
@click.version_option(prog_name='vibe-check')
def main(file_path: Optional[str], output: Optional[str],
         api_key: Optional[str], setup_key: bool):
    """
    🔍 VIBE CHECK - Security Analysis Tool

    Analyze code files for security vulnerabilities using Claude 4.

    Examples:
        vibe-check app.py
        vibe-check src/main.js --output custom_report.md
        vibe-check --api-key sk-... vulnerable_code.py
    """
    console.print(Panel.fit(
        "[bold blue]🔍 VIBE CHECK[/bold blue]\n"
        "[dim]Security Analysis Tool powered by Claude 4[/dim]",
        border_style="blue"
    ))

    try:
        # Handle setup mode
        if setup_key:
            _ = load_api_key()  # This will force a prompt for the API key
            console.print("\n✨ [bold green]Setup complete![/bold green]")
            sys.exit(0)

        # Ensure we have a file path for analysis
        if not file_path:
            raise click.UsageError(
                "Please provide a file path to analyze, or use --setup to "
                "configure your API key."
            )

        # Load API key
        if api_key:
            current_api_key = api_key
        else:
            current_api_key = load_api_key()

        # Validate input file
        input_path = validate_file_path(file_path)

        # Determine output path
        if output:
            output_path = Path(output)
        else:
            output_path = generate_report_filename(input_path)

        console.print(f"📁 Analyzing: [bold]{input_path}[/bold]")
        console.print(f"📄 Report will be saved to: [bold]{output_path}[/bold]")
        console.print()

        # Initialize analyzer
        analyzer = SecurityAnalyzer(current_api_key)

        # Perform analysis with progress indicator
        analysis_result, start_time, end_time = perform_analysis(
            analyzer, input_path
        )

        # Write report
        write_report(output_path, input_path, analysis_result,
                     start_time, end_time)

        # Success message
        console.print("✅ [bold green]Analysis complete![/bold green]")
        console.print(
            f"📊 Security report saved to: [bold cyan]{output_path}[/bold cyan]"
        )
        console.print(
            f"⏱️  Analysis took: [dim]{end_time - start_time:.2f} seconds[/dim]"
        )

    except click.Abort:
        console.print("❌ [yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except click.ClickException as exc:
        console.print(f"❌ [bold red]Error:[/bold red] {exc.message}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n❌ [yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except (OSError, RuntimeError) as exc:
        console.print(f"❌ [bold red]Unexpected error:[/bold red] {exc}")
        sys.exit(1)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
