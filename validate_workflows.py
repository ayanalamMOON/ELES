#!/usr/bin/env python3
"""
GitHub Actions Workflow Validator
Tests all workflow files for common issues and validates structure.
"""

import os
import yaml
import re
from pathlib import Path

def validate_workflow(file_path):
    """Validate a GitHub Actions workflow file."""
    print(f"\n🔍 Validating {file_path}")

    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            workflow = yaml.safe_load(content)

        # Check required top-level keys
        if 'name' not in workflow:
            issues.append("Missing 'name' field")

        if 'on' not in workflow:
            issues.append("Missing 'on' trigger field")

        if 'jobs' not in workflow:
            issues.append("Missing 'jobs' field")

        # Check for common action version issues
        action_patterns = [
            (r'actions/checkout@v(\d+)', 'actions/checkout should use v4'),
            (r'actions/setup-python@v(\d+)', 'actions/setup-python should use v4 or v5'),
            (r'actions/cache@v(\d+)', 'actions/cache should use v4'),
            (r'actions/upload-artifact@v(\d+)', 'actions/upload-artifact should use v4'),
            (r'actions/download-artifact@v(\d+)', 'actions/download-artifact should use v4')
        ]

        for pattern, message in action_patterns:
            matches = re.findall(pattern, content)
            for version in matches:
                if int(version) < 4:
                    issues.append(f"{message} (found v{version})")

        # Check for jobs structure
        if 'jobs' in workflow:
            for job_name, job_config in workflow['jobs'].items():
                if 'runs-on' not in job_config:
                    issues.append(f"Job '{job_name}' missing 'runs-on'")

                if 'steps' not in job_config:
                    issues.append(f"Job '{job_name}' missing 'steps'")
                elif not isinstance(job_config['steps'], list):
                    issues.append(f"Job '{job_name}' steps should be a list")

        # Check for environment variables best practices
        if 'PYTHONPATH' in content and 'export PYTHONPATH=' not in content:
            issues.append("Consider using 'export PYTHONPATH=' for better compatibility")

        # Check for security best practices
        if '${{ secrets.' in content:
            print("  ℹ️  Found secrets usage - ensure all secrets are properly configured")

        # Report results
        if issues:
            print("  ❌ Issues found:")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print("  ✅ No issues found")
            return True

    except yaml.YAMLError as e:
        print(f"  ❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Main validation function."""
    print("🚀 GitHub Actions Workflow Validator")
    print("=" * 50)

    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return

    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))

    if not workflow_files:
        print("❌ No workflow files found")
        return

    print(f"Found {len(workflow_files)} workflow files")

    all_valid = True
    for file_path in sorted(workflow_files):
        is_valid = validate_workflow(file_path)
        all_valid = all_valid and is_valid

    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All workflows validated successfully!")
    else:
        print("⚠️  Some workflows have issues that need attention")

    # Additional checks
    print("\n📋 Additional Recommendations:")
    print("  • Enable branch protection rules requiring status checks")
    print("  • Configure repository secrets: PYPI_API_TOKEN, CODECOV_TOKEN")
    print("  • Review workflow triggers to match your branching strategy")
    print("  • Consider enabling Dependabot for automated dependency updates")

if __name__ == "__main__":
    main()
