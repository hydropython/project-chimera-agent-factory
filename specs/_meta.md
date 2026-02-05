cat > specs/_meta.md << 'EOF'
# Project Chimera: Meta Specification

## Vision Statement
Create a factory that produces autonomous AI influencers capable of:
1. Researching social media trends in real-time
2. Generating high-quality, platform-optimized content
3. Managing multi-platform engagement autonomously
4. Self-optimizing based on performance metrics

## Core Constraints
1. **Safety First**: All content must pass through a human-in-the-loop safety layer before publication
2. **Platform Compliance**: Must adhere to all platform TOS and content guidelines
3. **Traceability**: Every action must be logged and traceable via MCP telemetry
4. **Scalability**: Architecture must support 1000+ concurrent agents

## Non-Negotiables
- No direct API calls to social platforms without rate limiting and error handling
- No content generation without safety checks
- No data persistence without proper encryption
- No agent deployment without comprehensive testing

## Success Metrics
- Content production velocity: 10+ pieces/day/agent
- Engagement rate: 5% minimum across platforms
- Safety compliance: 100% human-reviewed before publication
- Uptime: 99.9% for critical path components

## Architectural Tenets
1. **Spec-Driven**: Code follows spec, never precedes it
2. **Agentic First**: Design for AI agents as primary users
3. **Observability**: Everything must be monitorable and debuggable
4. **Resilience**: Graceful degradation under failure conditions
EOF
