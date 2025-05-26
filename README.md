# 🔍 Vibe Security AI - AI-Powered Security Analysis CLI

[![PyPI version](https://badge.fury.io/py/vibe-security-ai.svg)](https://badge.fury.io/py/vibe-security-ai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional command-line tool that leverages Claude 4 Sonnet to perform comprehensive security analysis on your code. Get detailed security reports with actionable recommendations to improve your code's security posture.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses Claude 4 Sonnet for intelligent security vulnerability detection
- 📊 **Comprehensive Reports**: Generates detailed markdown reports with risk assessments
- 🎯 **Multi-Language Support**: Analyzes 20+ programming languages
- 🚀 **Professional CLI**: Beautiful, rich terminal interface with progress indicators
- ⚡ **Fast & Efficient**: Quick analysis with detailed feedback
- 🔧 **Flexible Output**: Custom output paths and automatic naming
- 📋 **Structured Analysis**: Executive summaries, detailed findings, and remediation roadmaps
- 🔒 **Privacy-Focused**: Local report generation with secure API communication

## 🚀 Quick Start

### Installation

```bash
pip install vibe-security-ai
```

### Setup

Configure your Anthropic API key ([Get one here](https://console.anthropic.com/)):

```bash
vibe-security-ai --setup
```

### Analyze Your Code

```bash
vibe-security-ai path/to/your/code.py
```

That's it! Your security report will be generated in the `security_reports/` folder.

## 📦 Installation Options

### Option 1: PyPI (Recommended)
```bash
pip install vibe-security-ai
```

### Option 2: Development Installation
```bash
git clone https://github.com/colesmcintosh/vibe-check.git
cd vibe-check
pip install -e .
```

## ⚙️ Configuration

### API Key Setup

Choose your preferred method:

**Interactive Setup (Recommended)**
```bash
vibe-security-ai --setup
```

**Environment Variable**
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

**`.env` File**
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## 🎯 Usage

### Basic Commands

```bash
# Analyze a file
vibe-security-ai app.py

# Custom output location
vibe-security-ai app.js --output custom_report.md
vibe-security-ai app.js -o custom_report.md

# Specify API key directly
vibe-security-ai script.php --api-key sk-your-key-here

# Get help
vibe-security-ai --help

# Check version
vibe-security-ai --version
```

### Real-World Examples

```bash
# Web application security audit
vibe-security-ai src/auth/login.py

# Frontend component analysis
vibe-security-ai components/UserProfile.tsx

# API endpoint security check
vibe-security-ai api/routes/users.js

# Database query analysis
vibe-security-ai models/user.sql

# Shell script security review
vibe-security-ai scripts/deploy.sh
```

## 🔧 Supported Languages

Vibe Security AI analyzes these file types:

| Category | Extensions |
|----------|------------|
| **Web Frontend** | `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`, `.scss`, `.vue`, `.svelte` |
| **Backend** | `.py`, `.java`, `.c`, `.cpp`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift` |
| **Mobile** | `.kt`, `.scala`, `.dart`, `.m`, `.mm` |
| **Scripts** | `.sh`, `.bash`, `.zsh`, `.sql`, `.pl`, `.lua` |
| **Other** | `.r`, `.nim`, `.zig` |

*Note: Any text file can be analyzed, with confirmation for unrecognized extensions.*

## 📊 Report Structure

Each security analysis includes:

### 📋 Executive Summary
- Overall security posture assessment
- Risk level classification (Critical/High/Medium/Low)
- Summary of findings by severity

### 🔍 Detailed Security Findings

**Critical Issues** 🚨
- Immediate security threats requiring urgent attention
- Potential for data breaches or system compromise

**High Priority** ⚠️
- Important vulnerabilities to address soon
- Significant security risks

**Medium Priority** 📝
- Issues for next development cycle
- Security improvements and hardening

**Low Priority** 💡
- Best practice recommendations
- Code quality and maintainability improvements

### 📊 Analysis Details
For each finding:
- Clear vulnerability description
- Exact code location (file and line numbers)
- Risk assessment and impact analysis
- Step-by-step remediation instructions
- Code examples showing fixes

### ✅ Security Recommendations
- Industry best practices
- Prevention strategies
- Compliance considerations (OWASP, CWE)
- Prioritized action plan

## 🖥️ CLI Output Examples

### Successful Analysis
```
🔍 VIBE SECURITY AI
Security Analysis Tool powered by Claude 4

📁 Analyzing: src/auth/login.py
📄 Report will be saved to: security_reports/login_security_report.md

🔎 Analyzing code for security vulnerabilities...

✅ Analysis complete!
📊 Security report saved to: security_reports/login_security_report.md
⏱️  Analysis took: 2.34 seconds
🔍 Found: 2 Critical, 1 High, 3 Medium, 2 Low priority issues
```

### Sample Report Header
```markdown
# Security Analysis Report

**File Analyzed:** `src/auth/login.py`
**Analysis Date:** 2024-01-15 14:30:22
**Analysis Duration:** 2.34 seconds
**Tool:** Vibe Security AI

---

## 🎯 Executive Summary

**Security Posture:** HIGH RISK ⚠️
**Total Issues Found:** 8
- 🚨 Critical: 2
- ⚠️ High: 1  
- 📝 Medium: 3
- 💡 Low: 2

This analysis identified several critical security vulnerabilities...
```

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"Anthropic API key not found"** | Run `vibe-security-ai --setup` or set `ANTHROPIC_API_KEY` environment variable |
| **"File not found"** | Check file path and permissions |
| **"API Error"** | Verify internet connection and API key validity |
| **"Permission denied"** | Check file read permissions and output directory write access |

### Getting Help

```bash
# Show detailed help
vibe-security-ai --help

# Check version
vibe-security-ai --version

# Test your setup
vibe-security-ai --setup
```

## 🏗️ Development

### Project Structure
```
vibe-security-ai/
├── vibe_check/
│   ├── __init__.py      # Package metadata
│   └── cli.py           # Main CLI application
├── pyproject.toml       # Modern Python packaging
├── requirements.txt     # Dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── CHANGELOG.md        # Version history
└── PUBLISHING.md       # Publishing guide
```

### Dependencies
- **click** (>=8.1.0,<9.0.0): CLI framework
- **anthropic** (>=0.34.0,<1.0.0): Claude API client  
- **rich** (>=13.0.0,<14.0.0): Terminal formatting

### Building from Source
```bash
# Clone repository
git clone https://github.com/colesmcintosh/vibe-check.git
cd vibe-check

# Install in development mode
pip install -e .

# Run tests
python test_package.py

# Build package
python -m build
```

## 🔒 Security & Privacy

- **Secure Communication**: All API calls use HTTPS encryption
- **No Data Storage**: Your code is not stored by the tool or Anthropic
- **Local Reports**: All analysis reports are saved locally only
- **API Privacy**: Review [Anthropic's Privacy Policy](https://www.anthropic.com/privacy) for API data handling
- **Open Source**: Full source code available for security review

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Here are some areas for improvement:

- 🌐 Additional programming language support
- 📋 Custom security rule definitions  
- 🔄 CI/CD pipeline integrations
- 📁 Batch file processing
- ⚙️ Configuration file support
- 🎨 Custom report templates

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/colesmcintosh/vibe-check/issues)
- 📖 **Documentation**: [GitHub Repository](https://github.com/colesmcintosh/vibe-check)
- 💬 **Questions**: Open a GitHub Discussion

## 🏷️ Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 🙏 Acknowledgments

- Built with [Claude 4](https://www.anthropic.com/) by Anthropic
- CLI framework powered by [Click](https://click.palletsprojects.com/)
- Beautiful terminal output via [Rich](https://rich.readthedocs.io/)

---

**Made with ❤️ for secure coding practices**

*Vibe Security AI - Because security shouldn't be an afterthought* 🛡️ 