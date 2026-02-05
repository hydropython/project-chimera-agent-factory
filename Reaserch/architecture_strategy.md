# Create the research directory if not exists
mkdir -p research

# Create the tooling strategy document
cat > research/tooling_strategy.md << 'EOF'
# Tooling Strategy: MCP Servers for Development

## Overview
This document outlines the Model Context Protocol (MCP) servers that will be used during development to enhance productivity, ensure traceability, and maintain consistency across the development environment.

## Core Development Philosophy
MCP servers are **development tools** used by humans and AI assistants during coding, NOT runtime tools used by the Chimera agents. They bridge our development environment with external services and provide enhanced capabilities.

## Required MCP Servers

### 1. Tenx MCP Sense (MANDATORY)
**Purpose**: Flight recorder for all development decisions and AI agent thinking
**Configuration**:
```json
{
  "mcpServers": {
    "tenx-sense": {
      "command": "npx",
      "args": ["@10xdev/sense", "--record", "project-chimera"]
    }
  }
}