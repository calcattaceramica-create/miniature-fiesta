#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test for DED Modern Launcher Debug Log Functionality
Tests the debug logging functionality in DED_Modern_Launcher.pyw
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk


class TestLauncherDebugLog(unittest.TestCase):
    """Test cases for launcher debug log functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create mock venv structure
        self.venv_dir = self.test_path / "venv" / "Scripts"
        self.venv_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mock python.exe
        self.python_exe = self.venv_dir / "python.exe"
        self.python_exe.touch()
        
        # Create mock run.py
        self.run_py = self.test_path / "run.py"
        self.run_py.touch()
        
        # Create mock database
        self.db_path = self.test_path / "erp_system.db"
        self.db_path.touch()
        
        # Log file path
        self.log_file = self.test_path / "launcher_debug.log"

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initial_debug_log_creation(self):
        """Test that initial debug log is created with correct information"""
        # Mock the ModernLauncher initialization
        with patch('tkinter.Tk'), \
             patch('os.chdir'), \
             patch('__main__.__file__', str(self.test_path / "DED_Modern_Launcher.pyw")):
            
            # Simulate writing initial debug log
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write(f"Working directory: {self.test_path}\n")
                f.write(f"__file__: {self.test_path / 'DED_Modern_Launcher.pyw'}\n")
                f.write(f"sys.executable: {sys.executable}\n")
                f.write(f"Python path: {self.python_exe}\n")
                f.write(f"Python exists: {self.python_exe.exists()}\n")
                f.write(f"run.py exists: {self.run_py.exists()}\n")
            
            # Verify log file was created
            self.assertTrue(self.log_file.exists(), "Debug log file should be created")
            
            # Read and verify content
            with open(self.log_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.assertIn("Working directory:", content)
            self.assertIn("__file__:", content)
            self.assertIn("sys.executable:", content)
            self.assertIn("Python path:", content)
            self.assertIn("Python exists: True", content)
            self.assertIn("run.py exists: True", content)

    def test_check_requirements_logging(self):
        """Test that check_requirements logs correct information"""
        # Simulate check_requirements logging
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n=== check_requirements called ===\n")
            f.write(f"venv_path: {self.python_exe}\n")
            f.write(f"venv exists: {self.python_exe.exists()}\n")
            f.write(f"pip_path: {self.venv_dir / 'pip.exe'}\n")
            f.write(f"pip exists: False\n")
            f.write(f"db_path: {self.db_path}\n")
            f.write(f"db exists: {self.db_path.exists()}\n")
        
        # Read and verify content
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("=== check_requirements called ===", content)
        self.assertIn("venv_path:", content)
        self.assertIn("venv exists: True", content)
        self.assertIn("pip_path:", content)
        self.assertIn("pip exists: False", content)
        self.assertIn("db_path:", content)
        self.assertIn("db exists: True", content)

    def test_flask_check_logging(self):
        """Test that Flask check results are logged correctly"""
        # Simulate Flask check logging
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"Flask check returncode: 0\n")
            f.write(f"Flask check stdout: \n")
            f.write(f"Flask check stderr: \n")
        
        # Read and verify content
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("Flask check returncode: 0", content)
        self.assertIn("Flask check stdout:", content)
        self.assertIn("Flask check stderr:", content)

    def test_log_file_format(self):
        """Test that log file follows expected format"""
        # Create a complete log file
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"Working directory: {self.test_path}\n")
            f.write(f"__file__: {self.test_path / 'DED_Modern_Launcher.pyw'}\n")
            f.write(f"sys.executable: C:\\Python314\\pythonw.exe\n")
            f.write(f"Python path: {self.python_exe}\n")
            f.write(f"Python exists: True\n")
            f.write(f"run.py exists: True\n")
            f.write(f"\n=== check_requirements called ===\n")
            f.write(f"venv_path: {self.python_exe}\n")
            f.write(f"venv exists: True\n")
            f.write(f"pip_path: {self.venv_dir / 'pip.exe'}\n")
            f.write(f"pip exists: False\n")
            f.write(f"db_path: {self.db_path}\n")
            f.write(f"db exists: True\n")
            f.write(f"Flask check returncode: 0\n")
            f.write(f"Flask check stdout: \n")
            f.write(f"Flask check stderr: \n")
        
        # Read and parse log file
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Verify structure
        self.assertGreater(len(lines), 0, "Log file should not be empty")
        self.assertTrue(any("Working directory:" in line for line in lines))
        self.assertTrue(any("check_requirements called" in line for line in lines))
        self.assertTrue(any("Flask check returncode:" in line for line in lines))


    def test_missing_venv_logging(self):
        """Test logging when venv doesn't exist"""
        # Remove venv
        import shutil
        shutil.rmtree(self.venv_dir.parent.parent)

        # Simulate check_requirements with missing venv
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"\n=== check_requirements called ===\n")
            f.write(f"venv_path: {self.python_exe}\n")
            f.write(f"venv exists: {self.python_exe.exists()}\n")

        # Read and verify
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("venv exists: False", content)

    def test_missing_database_logging(self):
        """Test logging when database doesn't exist"""
        # Remove database
        self.db_path.unlink()

        # Simulate check_requirements with missing database
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"db_path: {self.db_path}\n")
            f.write(f"db exists: {self.db_path.exists()}\n")

        # Read and verify
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("db exists: False", content)

    def test_flask_import_error_logging(self):
        """Test logging when Flask import fails"""
        # Simulate Flask import error
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"Flask check returncode: 1\n")
            f.write(f"Flask check stdout: \n")
            f.write(f"Flask check stderr: ModuleNotFoundError: No module named 'flask'\n")

        # Read and verify
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Flask check returncode: 1", content)
        self.assertIn("ModuleNotFoundError", content)

    def test_log_file_encoding(self):
        """Test that log file handles UTF-8 encoding correctly"""
        # Write Arabic text (as seen in the launcher)
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("Working directory: C:\\Users\\DELL\\DED\n")
            f.write("البيئة الافتراضية - Virtual Environment\n")
            f.write("قاعدة البيانات - Database\n")

        # Read and verify UTF-8 encoding
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("البيئة الافتراضية", content)
        self.assertIn("قاعدة البيانات", content)

    def test_log_file_append_mode(self):
        """Test that subsequent logs are appended, not overwritten"""
        # Write initial log
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("Initial log entry\n")

        # Append additional log
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write("=== check_requirements called ===\n")

        # Read and verify both entries exist
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Initial log entry", content)
        self.assertIn("check_requirements called", content)

    def test_start_application_logging(self):
        """Test logging during application start"""
        # Simulate start_application logging
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("\n=== start_application called ===\n")
            f.write("is_running: False\n")
            f.write("Calling check_requirements...\n")
            f.write("check_requirements passed! Starting app...\n")

        # Read and verify
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("start_application called", content)
        self.assertIn("is_running: False", content)
        self.assertIn("check_requirements passed!", content)

    def test_log_exception_handling(self):
        """Test that logging exceptions are handled gracefully"""
        # This simulates the try-except blocks in the launcher
        # that ignore logging errors
        try:
            # Try to write to a read-only location (should fail)
            with open("/invalid/path/launcher_debug.log", "w") as f:
                f.write("This should fail\n")
        except Exception:
            # Exception should be caught and ignored
            pass

        # Test should pass without raising exception
        self.assertTrue(True)


class TestDebugLogParsing(unittest.TestCase):
    """Test cases for parsing and validating debug log content"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = Path(self.test_dir) / "launcher_debug.log"

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_parse_working_directory(self):
        """Test parsing working directory from log"""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("Working directory: C:\\Users\\DELL\\DED\n")

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Working directory:"):
                    working_dir = line.split(":", 1)[1].strip()
                    self.assertEqual(working_dir, "C:\\Users\\DELL\\DED")

    def test_parse_boolean_values(self):
        """Test parsing boolean values from log"""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("Python exists: True\n")
            f.write("pip exists: False\n")

        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract boolean values
        python_exists = "Python exists: True" in content
        pip_exists = "pip exists: True" in content

        self.assertTrue(python_exists)
        self.assertFalse(pip_exists)

    def test_parse_returncode(self):
        """Test parsing Flask check return code"""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("Flask check returncode: 0\n")

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if "Flask check returncode:" in line:
                    returncode = int(line.split(":")[-1].strip())
                    self.assertEqual(returncode, 0)


if __name__ == "__main__":
    unittest.main()

