import platform
import shutil
import sys

def check_poppler():
    print("Checking for Poppler...")
    pdfinfo_path = shutil.which("pdfinfo")

    if pdfinfo_path:
        print(f"✅ Poppler is installed at: {pdfinfo_path}")
        return

    print("❌ Poppler (pdfinfo) is NOT installed or not in PATH.\n")
    os_name = platform.system()

    if os_name == "Windows":
        print("👉 Windows instructions:")
        print("""
1. Download Poppler for Windows:
   https://github.com/oschwartz10612/poppler-windows/releases/

2. Extract the ZIP (e.g., to C:\\poppler)

3. Add C:\\poppler\\bin to your System PATH:
   - Press Win + S and type 'Environment Variables'
   - Edit the 'Path' system variable and add the above path

4. Restart your terminal or IDE

5. Test in terminal:
   pdfinfo --version
        """)
    elif os_name == "Darwin":
        print("👉 macOS instructions:")
        print("""
Run in Terminal:

    brew install poppler
        """)
    elif os_name == "Linux":
        print("👉 Linux instructions (Debian/Ubuntu):")
        print("""
Run in Terminal:

    sudo apt update
    sudo apt install poppler-utils
        """)
    else:
        print("❓ Unsupported or unknown OS. Please install Poppler manually.")

if __name__ == "__main__":
    check_poppler()