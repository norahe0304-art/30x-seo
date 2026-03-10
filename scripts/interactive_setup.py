#!/usr/bin/env python3
"""
Guided first-run setup wizard for 30x SEO.

Walks the user through installing dependencies, configuring API credentials,
and validating the installation.

Usage:
    python interactive_setup.py
    python interactive_setup.py --non-interactive
"""

import argparse
import base64
import importlib
import os
import subprocess
import sys
from pathlib import Path


def find_project_root() -> Path:
    """Find the 30x-seo project root."""
    candidates = [
        Path(__file__).parent.parent,
        Path.cwd(),
        Path.home() / "30x-seo",
    ]
    for p in candidates:
        if (p / "seo" / "SKILL.md").exists() or (p / "skills").is_dir():
            return p
    return candidates[0]


PROJECT_ROOT = find_project_root()

REQUIRED_DEPS = {
    "beautifulsoup4": "bs4",
    "requests": "requests",
    "lxml": "lxml",
    "Pillow": "PIL",
    "urllib3": "urllib3",
    "validators": "validators",
}


def print_header(text: str):
    """Print a section header."""
    print()
    print("=" * 50)
    print(f"  {text}")
    print("=" * 50)
    print()


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question, return True for yes."""
    suffix = "[Y/n]" if default else "[y/N]"
    try:
        answer = input(f"{question} {suffix}: ").strip().lower()
    except EOFError:
        return default
    if not answer:
        return default
    return answer in ("y", "yes")


def check_and_install_deps() -> list[str]:
    """Check required Python dependencies. Return list of missing ones."""
    missing = []
    for pkg_name, import_name in REQUIRED_DEPS.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pkg_name)
    return missing


def step_python_deps():
    """Step 1: Check and optionally install Python dependencies."""
    print_header("Step 1: Python Dependencies")

    missing = check_and_install_deps()

    if not missing:
        print("All required Python packages are installed.")
        return

    print(f"Missing packages: {', '.join(missing)}")
    print()

    if prompt_yes_no("Install missing packages now?"):
        requirements_file = PROJECT_ROOT / "requirements.txt"
        if requirements_file.exists():
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
            print(f"Running: {' '.join(cmd)}")
            print()
            try:
                subprocess.run(cmd, check=True)
                print()
                print("Dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print()
                print("ERROR: pip install failed. Try manually:")
                print(f"  pip install -r {requirements_file}")
        else:
            cmd = [sys.executable, "-m", "pip", "install"] + missing
            print(f"Running: {' '.join(cmd)}")
            print()
            try:
                subprocess.run(cmd, check=True)
                print()
                print("Dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print()
                print("ERROR: pip install failed. Try manually:")
                print(f"  pip install {' '.join(missing)}")
    else:
        print("Skipping. You can install later with:")
        print(f"  pip install -r {PROJECT_ROOT / 'requirements.txt'}")


def step_dataforseo():
    """Step 2: Configure DataForSEO credentials."""
    print_header("Step 2: DataForSEO API (optional)")

    print("DataForSEO powers keyword research, backlink analysis, SERP data,")
    print("and AI visibility checks. You can skip this and add it later.")
    print()

    auth_path = Path.home() / ".config" / "dataforseo" / "auth"

    if auth_path.exists():
        content = auth_path.read_text().strip()
        if len(content) > 10:
            print(f"Existing credentials found at {auth_path}")
            if not prompt_yes_no("Overwrite existing credentials?", default=False):
                print("Keeping existing credentials.")
                return

    if not prompt_yes_no("Configure DataForSEO credentials?"):
        print("Skipping DataForSEO setup.")
        return

    print()
    print("Enter your DataForSEO login and password.")
    print("These will be base64-encoded and saved locally.")
    print()

    try:
        login = input("DataForSEO login (email): ").strip()
        password = input("DataForSEO password: ").strip()
    except EOFError:
        print("Skipping.")
        return

    if not login or not password:
        print("Login and password are required. Skipping.")
        return

    encoded = base64.b64encode(f"{login}:{password}".encode()).decode()

    auth_path.parent.mkdir(parents=True, exist_ok=True)
    auth_path.write_text(encoded)
    os.chmod(str(auth_path), 0o600)

    print()
    print(f"Credentials saved to {auth_path}")


def step_google_api():
    """Step 3: Configure Google API key."""
    print_header("Step 3: Google API Key (optional)")

    print("A Google API key enables real Core Web Vitals data via CrUX API")
    print("and PageSpeed Insights. You can skip this and add it later.")
    print()

    key_path = Path.home() / ".config" / "google" / "api_key"

    if key_path.exists():
        print(f"Existing API key found at {key_path}")
        if not prompt_yes_no("Overwrite existing key?", default=False):
            print("Keeping existing key.")
            return

    if not prompt_yes_no("Configure Google API key?"):
        print("Skipping Google API setup.")
        return

    print()
    print("Get a key from: https://console.cloud.google.com/apis/credentials")
    print("Enable: PageSpeed Insights API, Chrome UX Report API")
    print()

    try:
        api_key = input("Google API key: ").strip()
    except EOFError:
        print("Skipping.")
        return

    if not api_key:
        print("No key entered. Skipping.")
        return

    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(api_key)
    os.chmod(str(key_path), 0o600)

    print()
    print(f"API key saved to {key_path}")


def step_playwright():
    """Step 4: Optionally install Playwright for screenshots."""
    print_header("Step 4: Playwright (optional)")

    print("Playwright enables visual regression screenshots and above-the-fold")
    print("analysis. It requires a ~200MB browser download.")
    print()

    try:
        importlib.import_module("playwright")
        print("Playwright is already installed.")
        return
    except ImportError:
        pass

    if not prompt_yes_no("Install Playwright for screenshot capabilities?"):
        print("Skipping Playwright. You can install later with:")
        print("  pip install playwright && playwright install chromium")
        return

    print()
    print("Installing Playwright...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright>=1.56.0,<2.0.0"],
            check=True,
        )
        print()
        print("Installing Chromium browser...")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
        )
        print()
        print("Playwright installed successfully.")
    except subprocess.CalledProcessError:
        print()
        print("ERROR: Playwright installation failed. Try manually:")
        print("  pip install playwright && playwright install chromium")


def step_health_check():
    """Step 5: Run health check to validate everything."""
    print_header("Step 5: Validation")

    health_check_script = PROJECT_ROOT / "scripts" / "health_check.py"

    if not health_check_script.exists():
        print(f"WARNING: health_check.py not found at {health_check_script}")
        print("Skipping validation.")
        return

    print("Running health check to validate your installation...")
    print()

    try:
        result = subprocess.run(
            [sys.executable, str(health_check_script), "--root", str(PROJECT_ROOT)],
            capture_output=False,
        )
        print()
        if result.returncode == 0:
            print("Setup complete! Your 30x SEO installation is ready.")
        else:
            print("Some issues were detected. Review the output above.")
            print("You can re-run the health check anytime with:")
            print(f"  python {health_check_script}")
    except Exception as e:
        print(f"ERROR running health check: {e}")


def run_non_interactive():
    """Non-interactive mode: validate existing configuration only."""
    print("30x SEO Setup — Non-Interactive Validation")
    print("=" * 50)
    print()

    # Check deps
    missing = check_and_install_deps()
    if missing:
        print(f"MISSING DEPS: {', '.join(missing)}")
        print(f"  Fix: pip install -r {PROJECT_ROOT / 'requirements.txt'}")
    else:
        print("Python deps: OK")

    # Check DataForSEO
    auth_path = Path.home() / ".config" / "dataforseo" / "auth"
    if auth_path.exists() and len(auth_path.read_text().strip()) > 10:
        print("DataForSEO:  OK")
    else:
        print("DataForSEO:  not configured (optional)")

    # Check Google API
    key_path = Path.home() / ".config" / "google" / "api_key"
    if key_path.exists() and key_path.read_text().strip():
        print("Google API:  OK")
    else:
        print("Google API:  not configured (optional)")

    # Check Playwright
    try:
        importlib.import_module("playwright")
        print("Playwright:  OK")
    except ImportError:
        print("Playwright:  not installed (optional)")

    print()

    # Run health check
    health_check_script = PROJECT_ROOT / "scripts" / "health_check.py"
    if health_check_script.exists():
        result = subprocess.run(
            [sys.executable, str(health_check_script), "--root", str(PROJECT_ROOT)],
            capture_output=False,
        )
        sys.exit(result.returncode)
    else:
        print("WARNING: health_check.py not found, cannot run full validation.")
        sys.exit(1 if missing else 0)


def main():
    parser = argparse.ArgumentParser(description="30x SEO guided setup wizard")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Validate existing config without prompts",
    )

    args = parser.parse_args()

    if args.non_interactive:
        run_non_interactive()
        return

    try:
        print_header("30x SEO — First-Run Setup")
        print("This wizard will help you configure your 30x SEO installation.")
        print("You can skip any step and configure it later.")
        print("Press Ctrl+C at any time to exit.")

        step_python_deps()
        step_dataforseo()
        step_google_api()
        step_playwright()
        step_health_check()

    except KeyboardInterrupt:
        print("\n\nSetup interrupted. You can re-run this wizard anytime with:")
        print(f"  python {Path(__file__).resolve()}")
        sys.exit(130)


if __name__ == "__main__":
    main()
