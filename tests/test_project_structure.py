"""Test that the project structure is set up correctly."""
import pytest
from pathlib import Path


def test_project_structure():
    """Test that all required directories and files exist."""
    project_root = Path(__file__).parent.parent
    
    # Check main package directories
    assert (project_root / "app").exists()
    assert (project_root / "app" / "__init__.py").exists()
    assert (project_root / "app" / "control_plane").exists()
    assert (project_root / "app" / "worker").exists()
    assert (project_root / "app" / "common").exists()
    
    # Check test directories
    assert (project_root / "tests").exists()
    assert (project_root / "tests" / "unit").exists()
    assert (project_root / "tests" / "integration").exists()
    assert (project_root / "tests" / "fixtures").exists()
    
    # Check configuration files
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / ".pre-commit-config.yaml").exists()
    assert (project_root / "pytest.ini").exists()
    assert (project_root / ".env.example").exists()
    assert (project_root / "README.md").exists()


def test_package_imports():
    """Test that the main packages can be imported."""
    import app
    import app.control_plane
    import app.worker
    import app.common
    
    assert app.__version__ == "0.1.0"


if __name__ == "__main__":
    test_project_structure()
    test_package_imports()
    print("✅ Project structure tests passed!")