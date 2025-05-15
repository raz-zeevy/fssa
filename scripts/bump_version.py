"""
Script to bump the version in lib/version.py
Usage: python bump_version.py [major|minor|patch|revision]
Default is to bump the revision (last number)
"""

import os
import re
import sys


def bump_version(version_type="revision"):
    # Path to version.py
    version_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "version.py"
    )

    # Read the current version
    with open(version_file, "r") as f:
        content = f.read()

    # Extract version
    version_match = re.search(
        r'__version__\s*=\s*"([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)"', content
    )

    if not version_match:
        print("Error: Could not find version in format MAJOR.MINOR.PATCH.REVISION")
        sys.exit(1)

    major, minor, patch, revision = map(int, version_match.groups())

    # Bump the appropriate part
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
        revision = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
        revision = 0
    elif version_type == "patch":
        patch += 1
        revision = 0
    else:  # revision
        revision += 1

    # Create new version string
    new_version = f"{major}.{minor}.{patch}.{revision}"

    # Replace the version in the file
    new_content = re.sub(
        r'(__version__\s*=\s*)"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"',
        r'\g<1>"' + new_version + '"',
        content,
    )

    # Write back to the file
    with open(version_file, "w") as f:
        f.write(new_content)

    print(f"Version bumped to {new_version}")
    return new_version


if __name__ == "__main__":
    version_type = "revision"
    if len(sys.argv) > 1:
        version_type = sys.argv[1].lower()
        if version_type not in ["major", "minor", "patch", "revision"]:
            print(f"Invalid version type: {version_type}")
            print("Usage: python bump_version.py [major|minor|patch|revision]")
            sys.exit(1)

    bump_version(version_type)
