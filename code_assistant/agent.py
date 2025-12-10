# Import necessary libraries
import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from .agent_tools import (
    analyze_code_structure, 
    check_security_issues,
    check_performance_issues,
    check_documentation,
)


# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

MODEL_GEMINI = "gemini-2.0-flash-exp"

# Security Agent
security_agent = Agent(
    name="security_agent",
    model=MODEL_GEMINI,
    description="Specialized in identifying security vulnerabilities in Python code.",
    instruction="""You are a security expert focused on Python code security.
    
    Use the 'check_security_issues' tool to analyze code for vulnerabilities.
    
    For each security issue found:
    1. Explain the risk clearly
    2. Provide severity assessment
    3. Suggest specific remediation
    4. Reference security best practices (OWASP, etc.)
    
    Be thorough but not alarmist. Distinguish between actual vulnerabilities and potential risks.""",
    tools=[check_security_issues]
)

# Performance Agent
performance_agent = Agent(
    name="performance_agent",
    model=MODEL_GEMINI,
    description="Specialized in identifying performance issues and optimization opportunities.",
    instruction="""You are a performance optimization expert for Python.
    
    Use the 'check_performance_issues' tool to analyze code.
    
    For each performance issue:
    1. Explain why it's inefficient
    2. Estimate potential impact
    3. Provide optimized alternative code
    4. Consider trade-offs (readability vs performance)
    
    Focus on meaningful optimizations, not micro-optimizations.""",
    tools=[check_performance_issues]
)

# Documentation Agent
documentation_agent = Agent(
    name="documentation_agent",
    model=MODEL_GEMINI,
    description="Specialized in reviewing code documentation quality and completeness.",
    instruction="""You are a documentation quality expert.
    
    Use the 'check_documentation' tool to analyze code documentation.
    
    For documentation issues:
    1. Identify what's missing or inadequate
    2. Explain why good documentation matters
    3. Provide example of good docstring for the code
    4. Follow Google Python Style Guide for docstrings
    
    Be constructive and educational.""",
    tools=[check_documentation]
)

root_agent = Agent(
    name="root_code_review_agent_v2",
    model=MODEL_GEMINI,
    description="Main code review coordinator that delegates to specialized review agents.",
    instruction="""You are the lead code reviewer coordinating a team of specialists.
    
    Your team consists of:
    1. 'security_agent': Reviews security vulnerabilities
    2. 'performance_agent': Analyzes performance issues
    3. 'documentation_agent': Checks documentation quality
    
    When reviewing code:
    1. Use 'analyze_code_structure' first to get overall structure
    2. Based on the review request, delegate to appropriate specialists:
       - Security concerns → security_agent
       - Performance review → performance_agent
       - Documentation check → documentation_agent
    3. You can call multiple specialists for comprehensive reviews
    4. Synthesize their feedback into a cohesive review
    
    Provide clear, actionable, and respectful feedback.""",
    tools=[analyze_code_structure],
    sub_agents=[security_agent, performance_agent, documentation_agent]
)

print(f"✅ Root agent '{root_agent.name}' created with sub-agents")