# 🤖 AI-Powered Code Review System

An intelligent, multi-agent code review system built with Google's Agent Development Kit (ADK) that automatically analyzes Python code for security vulnerabilities, performance issues, and documentation quality.

## 📋 Overview

This project implements a team of specialized AI agents that collaborate to provide comprehensive code reviews. The system uses Google's Gemini models and demonstrates advanced agentic AI patterns including delegation, tool use, and multi-agent coordination.

**Key Features:**
- 🔒 **Security Analysis**: Detects hardcoded secrets, unsafe function calls, and common vulnerabilities
- ⚡ **Performance Review**: Identifies inefficient patterns and suggests optimizations
- 📝 **Documentation Check**: Validates docstring presence and quality
- 🏗️ **Structure Analysis**: Uses AST parsing to extract code metrics and complexity
- 🤝 **Multi-Agent Coordination**: Root agent intelligently delegates to specialized reviewers

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Root Code Review Agent            │
│   (Coordinator)                     │
└───────────┬─────────────────────────┘
            │
    ┌───────┴───────┬─────────────────┐
    │               │                 │
    ▼               ▼                 ▼
┌─────────┐   ┌──────────┐   ┌──────────────┐
│Security │   │Performance│  │Documentation │
│ Agent   │   │  Agent    │  │   Agent      │
└─────────┘   └──────────┘   └──────────────┘
     │              │                │
     ▼              ▼                ▼
┌─────────────────────────────────────────┐
│            Tool Layer                    │
│  • check_security_issues()              │
│  • check_performance_issues()           │
│  • check_documentation()                │
│  • analyze_code_structure()             │
└─────────────────────────────────────────┘
```