import sys
import subprocess
import os

from PySide6.QtWidgets import QMessageBox, QApplication

def install_and_restart(packages, parent=None):
    """
    Installs the specified pip packages and restarts the current script.
    packages: list of package names (str)
    parent: parent QWidget for dialogs (optional)
    """
    if not packages:
        return

    # Confirm with the user
    pkg_list = "\n".join(packages)
    app = QApplication.instance() or QApplication(sys.argv)
    reply = QMessageBox.question(
        parent, "Install Required Packages",
        f"The following packages will be installed/updated:\n\n{pkg_list}\n\nContinue?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        return

    try:
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    except Exception as e:
        QMessageBox.critical(parent, "Pip Install Failed", f"Failed to install packages:\n{e}")
        return

    QMessageBox.information(parent, "Restarting", "The application will now restart to apply changes.")
    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)

def ensure_packages(packages, parent=None):
    """
    Checks if packages are installed, and if not, runs install_and_restart.
    Returns True if all packages are present, False if installation/restart was triggered.
    """
    import importlib.util
    missing = []
    for pkg in packages:
        # If package has extra (e.g. PySide6[gui]), just check base
        base_pkg = pkg.split("[")[0]
        if importlib.util.find_spec(base_pkg) is None:
            missing.append(pkg)
    if missing:
        install_and_restart(missing, parent)
        return False
    return True

# Example usage:
# if __name__ == "__main__":
#     ensure_packages(["PySide6"])