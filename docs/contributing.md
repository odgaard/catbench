# Contributing to CATBench

We welcome contributions to CATBench! This guide will help you get started.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/catbench.git
cd catbench
git remote add upstream https://github.com/odgaard/catbench.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Project Structure

```
catbench/
├── __init__.py          # Package initialization
├── main.py              # Core benchmark interface
├── benchmarks/          # Benchmark implementations
│   ├── __init__.py
│   ├── taco.py         # TACO benchmark base class
│   ├── rise.py         # RISE benchmark base class
│   ├── spmm.py         # SpMM benchmark
│   └── ...             # Other benchmarks
├── utils/              # Utility functions
└── tests/              # Test files
```

## Adding a New Benchmark

### 1. Create Benchmark File

Create a new file in `catbench/benchmarks/`:

```python
# catbench/benchmarks/mybenchmark.py
from catbench.benchmarks.base import BaseBenchmark

class MyBenchmark(BaseBenchmark):
    def __init__(self):
        super().__init__()
        self.name = "mybenchmark"
        self.suite = "custom"  # or "taco"/"rise"
        
    def get_parameters(self):
        """Define benchmark parameters."""
        return {
            'param1': {
                'type': int,
                'range': [1, 100],
                'default': 10,
                'description': 'First parameter'
            },
            'param2': {
                'type': str,
                'choices': ['option1', 'option2'],
                'default': 'option1',
                'description': 'Second parameter'
            }
        }
    
    def validate_config(self, config):
        """Validate configuration parameters."""
        params = self.get_parameters()
        for key, spec in params.items():
            if key not in config:
                raise ValueError(f"Missing required parameter: {key}")
            
            value = config[key]
            if spec['type'] == int and not isinstance(value, int):
                raise TypeError(f"{key} must be an integer")
            
            if 'range' in spec:
                min_val, max_val = spec['range']
                if not min_val <= value <= max_val:
                    raise ValueError(f"{key} must be between {min_val} and {max_val}")
                    
            if 'choices' in spec and value not in spec['choices']:
                raise ValueError(f"{key} must be one of {spec['choices']}")
    
    def format_query(self, config, fidelity):
        """Format configuration for execution."""
        # Convert Python config to execution format
        return {
            'benchmark': self.name,
            'config': config,
            'fidelity': fidelity
        }
```

### 2. Register Benchmark

Add to `catbench/benchmarks/__init__.py`:

```python
from .mybenchmark import MyBenchmark

BENCHMARKS = {
    # ... existing benchmarks ...
    'mybenchmark': MyBenchmark,
}
```

### 3. Add Tests

Create `tests/test_mybenchmark.py`:

```python
import pytest
import catbench as cb

def test_mybenchmark_creation():
    bench = cb.benchmark('mybenchmark')
    assert bench is not None

def test_mybenchmark_validation():
    bench = cb.benchmark('mybenchmark')
    
    # Valid config
    valid_config = {'param1': 50, 'param2': 'option1'}
    bench.validate_config(valid_config)  # Should not raise
    
    # Invalid configs
    with pytest.raises(ValueError):
        bench.validate_config({'param1': 200})  # Out of range
    
    with pytest.raises(TypeError):
        bench.validate_config({'param1': 'not_an_int', 'param2': 'option1'})

def test_mybenchmark_query():
    bench = cb.benchmark('mybenchmark', dataset='test')
    config = {'param1': 10, 'param2': 'option1'}
    fidelity = {'iterations': 5}
    
    result = bench.query(config, fidelity)
    assert 'compute_time' in result
    assert isinstance(result['compute_time'], (int, float))
```

### 4. Add Documentation

Update relevant documentation files:
- Add to `docs/benchmarks.md`
- Add examples to `docs/examples.md`
- Update API reference if needed

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_mybenchmark.py

# Run with coverage
pytest --cov=catbench --cov-report=html
```

### Test Guidelines

1. Test all new functionality
2. Include both positive and negative test cases
3. Test edge cases and error conditions
4. Aim for >80% code coverage

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def my_function(param1: int, param2: str) -> dict:
    """Brief description of function.
    
    Longer description if needed, explaining the purpose
    and behavior of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is negative
        TypeError: When param2 is not a string
        
    Example:
        >>> result = my_function(10, "test")
        >>> print(result['status'])
        'success'
    """
    pass
```

### Update Documentation

When adding features:
1. Update docstrings
2. Update relevant .md files in `docs/`
3. Add examples if applicable
4. Update README.md if it's a major feature

## Submitting Changes

### 1. Commit Your Changes

```bash
# Make sure tests pass
pytest

# Format and lint
black catbench/
flake8 catbench/

# Commit with descriptive message
git add .
git commit -m "Add MyBenchmark implementation

- Implement MyBenchmark class with param1 and param2
- Add validation for parameter ranges
- Include comprehensive test coverage
- Update documentation"
```

### 2. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference any related issues
- List of changes made
- Test results/coverage

### 3. Code Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Update your branch if needed:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
4. Once approved, your PR will be merged

## Release Process

Releases are managed by maintainers:

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v0.2.0 -m "Release version 0.2.0"`
4. Push to PyPI: `python setup.py sdist bdist_wheel && twine upload dist/*`

## Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers (see README)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

Thank you for contributing to CATBench!
