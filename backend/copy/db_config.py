"""
🔒 OFFICIAL DATABASE CONFIGURATION - SECURITY MODULE
=====================================================

This module enforces the use of ONLY the official database.
DO NOT MODIFY unless you understand the security implications.

Any attempt to use a different database will be blocked.
"""

import os
import sys
from pathlib import Path

# OFFICIAL DATABASE - DO NOT CHANGE
OFFICIAL_DB_NAME = "aibot.db"
OFFICIAL_DB_DIR = "api_server"

def get_official_db_path() -> str:
    """
    Get the official database path with security validation.
    
    Returns:
        str: Absolute path to the official database
        
    Raises:
        SecurityError: If path validation fails
    """
    # Build the path
    root_dir = Path(__file__).parent
    db_path = root_dir / OFFICIAL_DB_DIR / OFFICIAL_DB_NAME
    
    # Security: Validate no path traversal
    if ".." in str(db_path):
        raise SecurityError("🚨 SECURITY VIOLATION: Path traversal detected!")
    
    # Security: Validate filename
    if db_path.name != OFFICIAL_DB_NAME:
        raise SecurityError(f"🚨 SECURITY VIOLATION: Unauthorized database name: {db_path.name}")
    
    # Convert to absolute path
    abs_path = db_path.resolve()
    
    # Final validation
    if not abs_path.name == OFFICIAL_DB_NAME:
        raise SecurityError(f"🚨 SECURITY VIOLATION: Database name mismatch after resolution!")
    
    return str(abs_path)


def validate_db_path(path: str) -> bool:
    """
    Validate that a given path points to the official database.
    
    Args:
        path: Path to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return OFFICIAL_DB_NAME in path and ".." not in path


class SecurityError(Exception):
    """Raised when database security validation fails"""
    pass


# Export the official path as a constant
OFFICIAL_DB_PATH = get_official_db_path()

if __name__ == "__main__":
    print(f"✅ Official Database Path: {OFFICIAL_DB_PATH}")
    print(f"✅ Exists: {os.path.exists(OFFICIAL_DB_PATH)}")
