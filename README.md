# Pytest Automation Framework

A comprehensive cross-platform test automation framework built with Python, Pytest, Selenium, and Appium for web and
mobile application testing.

**📊 [Live Test Reports](https://aquariux.netlify.app/)** - View real-time test execution results, detailed test cases, screenshots, and performance metrics.

## 📋 Prerequisites

* __Python 3.10+__ installed
* __NodeJS__ installed
* __FFmpeg__ installed for video recording

## 🛠️ Installation

1. **Project Setup**

* Set up a Python virtual environment directory

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* Install necessary libraries

    ```bash
    pip3 install -r requirements.txt
    ```

2. **Install Allure commandline tool**
   ```bash
   npm install -g allure-commandline
   ```

4. **Install FFmpeg** (macOS)
   ```bash
   brew install ffmpeg
   ```

## ⚙️ Configuration

### Environment Configuration

The framework uses environment-based configuration. Create your environment file in `config/` directory

## 🏗️ Project Structure

```
Aquariux/
├── config/                     # Configuration files
│   └── config.yaml             # Environment configuration
├── src/                        # Source code
│   ├── apps/                   # Application-specific code
│   │   ├── mobile/             # Mobile app components
│   │   │   └── screen/         # Mobile screen objects
│   │   └── web/                # Web app components
│   │       ├── component/      # Reusable UI components
│   │       ├── page/           # Page Object Models
│   │       └── popup/          # Popup/dialog components
│   ├── data_object/            # Data models
│   ├── enums/                  # Enumeration definitions
│   ├── utils/                  # Utility functions
│   ├── consts.py               # Constants
│   ├── data_runtime.py         # Runtime data management
│   ├── web_container.py        # Web application container
│   └── mobile_container.py     # Mobile application container
├── tests/                      # Test files
│   ├── conftest.py             # Pytest configuration
│   └── web/                    # Web tests
│       ├── credential/         # Authentication tests
│       └── trader/             # Trading functionality tests
├── allure-report/              # Allure test reports
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── WIDGET_CONVENTION.md        # Widget conventions documentation
└── README.md                   # Project documentation
```

## 🚀 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/web/credential/test_TC01.py

# Run specific test function
pytest tests/web/credential/test_TC1.py::test_login_with_valid_credential
```

### Command Line Options

```bash
# Run with specific environment
pytest --env=config

# Run with debug logging
pytest --debuglog

# Run with video recording
pytest --record

# Run in headless mode
pytest --headless

# Run with specific browser
pytest --browser=firefox

# Run with custom credentials
pytest --user=testuser --password=testpass

# Run in remote mode
pytest --remote
```

### Allure Reports

```bash
# Generate Allure report
pytest --alluredir=./allure-results

# View Allure report
allure serve ./allure-results

# Generate static HTML report
allure generate ./allure-results --clean
```

## 🐛 Debugging

### Debug Logging

```bash
pytest --debuglog
```

### Screenshot Capture

Screenshots are automatically captured on test failures and attached to Allure reports.

### Video Recording

```bash
pytest --record
```

## 📝 Best Practices

1. **Test Organization**: Group tests by functionality in appropriate directories
2. **Page Objects**: Keep page objects clean and focused on UI interactions
3. **Assertions**: Use the `verify()` utility for enhanced failure reporting
4. **Logging**: Use descriptive step logging for better test documentation
5. **Configuration**: Externalize environment-specific configurations
6. **Data Management**: Use data objects for structured test data

---

**Note**: This framework is designed for cross-platform testing with a focus on web and mobile applications. Ensure all
prerequisites are installed and configured before running tests. 