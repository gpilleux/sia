#!/usr/bin/env python3
"""
MCP Server for DIPRES Analyzer tools.
Exposes project-specific capabilities to GitHub Copilot CLI.

Usage:
    # Configure in ~/.copilot/mcp-config.json:
    {
      "mcpServers": {
        "dipres-analyzer-tools": {
          "command": "python",
          "args": ["/path/to/dipres_analyzer/skills/mcp_server.py"],
          "env": {
            "DATABASE_URL": "${DATABASE_URL}",
            "OPENAI_API_KEY": "${OPENAI_API_KEY}"
          }
        }
      }
    }
    
    # Then use from Copilot CLI:
    copilot --additional-mcp-config ~/.copilot/mcp-config.json
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Project root (assumes script is in skills/)
PROJECT_ROOT = Path(__file__).parent.parent


class DipresAnalyzerMcpServer:
    """Custom MCP server for DIPRES Analyzer project tools."""
    
    def __init__(self):
        self.project_root = PROJECT_ROOT
        
    @property
    def tools(self) -> Dict[str, Any]:
        """Available tools exposed to Copilot CLI."""
        return {
            "run_e2e_test": {
                "description": "Execute E2E test suite and return results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_file": {
                            "type": "string",
                            "description": "Test file to run (default: clean_and_test.py)",
                            "default": "clean_and_test.py"
                        }
                    }
                }
            },
            "check_ddd_compliance": {
                "description": "Verify DDD layer separation and entity immutability",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "strict": {
                            "type": "boolean",
                            "description": "Enable strict mode (fails on any violation)",
                            "default": False
                        }
                    }
                }
            },
            "visualize_architecture": {
                "description": "Generate dependency diagram",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["svg", "png", "pdf"],
                            "description": "Output format",
                            "default": "svg"
                        }
                    }
                }
            },
            "check_complexity": {
                "description": "Analyze code complexity using radon",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "threshold": {
                            "type": "integer",
                            "description": "Cyclomatic complexity threshold",
                            "default": 10
                        }
                    }
                }
            },
            "check_coverage": {
                "description": "Run tests with coverage analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "min_coverage": {
                            "type": "integer",
                            "description": "Minimum coverage percentage",
                            "default": 80
                        }
                    }
                }
            }
        }
    
    async def handle_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool and return result."""
        handlers = {
            "run_e2e_test": self._run_e2e_test,
            "check_ddd_compliance": self._check_ddd_compliance,
            "visualize_architecture": self._visualize_architecture,
            "check_complexity": self._check_complexity,
            "check_coverage": self._check_coverage
        }
        
        handler = handlers.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            return await handler(parameters)
        except Exception as e:
            return {"error": str(e), "tool": tool_name}
    
    async def _run_e2e_test(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run E2E test suite."""
        test_file = params.get("test_file", "clean_and_test.py")
        
        cmd = f"cd {self.project_root} && docker compose exec -T backend python {test_file}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "success": proc.returncode == 0,
            "test_file": test_file,
            "output": stdout.decode() if stdout else "",
            "errors": stderr.decode() if stderr else None,
            "exit_code": proc.returncode
        }
    
    async def _check_ddd_compliance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Check DDD layer separation."""
        strict = params.get("strict", False)
        
        cmd = f"cd {self.project_root} && ./skills/check_ddd_compliance.sh {'true' if strict else 'false'}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "compliant": proc.returncode == 0,
            "strict_mode": strict,
            "output": stdout.decode() if stdout else "",
            "violations": stderr.decode() if stderr else None,
            "exit_code": proc.returncode
        }
    
    async def _visualize_architecture(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate architecture diagram."""
        output_format = params.get("format", "svg")
        
        cmd = f"cd {self.project_root} && ./skills/visualize_architecture.sh --format={output_format}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        output_file = stdout.decode().strip() if stdout else None
        
        return {
            "success": proc.returncode == 0,
            "output_file": output_file,
            "format": output_format,
            "errors": stderr.decode() if stderr else None,
            "exit_code": proc.returncode
        }
    
    async def _check_complexity(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code complexity."""
        threshold = params.get("threshold", 10)
        
        cmd = f"cd {self.project_root} && ./skills/check_complexity.sh {threshold}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "success": proc.returncode == 0,
            "threshold": threshold,
            "output": stdout.decode() if stdout else "",
            "errors": stderr.decode() if stderr else None,
            "exit_code": proc.returncode
        }
    
    async def _check_coverage(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run tests with coverage analysis."""
        min_coverage = params.get("min_coverage", 80)
        
        cmd = f"cd {self.project_root} && ./skills/check_coverage.sh {min_coverage}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "success": proc.returncode == 0,
            "min_coverage": min_coverage,
            "output": stdout.decode() if stdout else "",
            "errors": stderr.decode() if stderr else None,
            "exit_code": proc.returncode
        }


async def main():
    """MCP Server main loop (JSON-RPC over stdio)."""
    server = DipresAnalyzerMcpServer()
    
    # Write server info to stderr for debugging
    sys.stderr.write(f"MCP Server started. Project root: {PROJECT_ROOT}\n")
    sys.stderr.flush()
    
    # Main loop: read JSON-RPC requests from stdin
    while True:
        try:
            # Read line from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            # Parse JSON-RPC request
            request = json.loads(line)
            
            # Handle request
            if request.get("method") == "tools/list":
                # List available tools
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": server.tools
                }
                
            elif request.get("method") == "tools/call":
                # Execute tool
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = await server.handle_tool_call(tool_name, arguments)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
                
            else:
                # Unknown method
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {request.get('method')}"
                    }
                }
            
            # Write response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            sys.stderr.write(f"JSON decode error: {e}\n")
            sys.stderr.flush()
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.flush()


if __name__ == "__main__":
    asyncio.run(main())
