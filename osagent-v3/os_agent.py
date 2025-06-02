#!/usr/bin/env python3
"""
Cross-Platform OS Agent using Gemini 1.5 Flash with Persistent Memory
A comprehensive system agent that can perform OS operations on Linux and Windows
with memory that persists across sessions. Browser automation components removed.
"""

import os
import sys
import subprocess
import platform
import json
import shutil
import psutil
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import google.generativeai as genai
from datetime import datetime
import logging
from dotenv import load_dotenv
import hashlib
import pickle
import asyncio

# Browser automation imports removed

# Langchain and Pydantic imports for browser automation removed
# from langchain_google_genai import ChatGoogleGenerativeAI
# from pydantic import BaseModel, Field

load_dotenv()

class MemoryManager:
    """Manages persistent memory for the OS Agent"""

    def __init__(self, memory_dir: str = "agent_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        # Database file for structured memory
        self.db_path = self.memory_dir / "agent_memory.db"

        # JSON file for quick access memory
        self.quick_memory_path = self.memory_dir / "quick_memory.json"

        # Initialize database
        self._init_database()

        # Load quick memory
        self.quick_memory = self._load_quick_memory()

        # Session ID for current session
        self.session_id = self._generate_session_id()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]

    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TEXT,
                    user_request TEXT,
                    agent_response TEXT,
                    execution_results TEXT,
                    system_state TEXT
                )
            ''')

            # System facts table (for learned information)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact_key TEXT UNIQUE,
                    fact_value TEXT,
                    timestamp TEXT,
                    session_id TEXT
                )
            ''')

            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preference_key TEXT UNIQUE,
                    preference_value TEXT,
                    timestamp TEXT
                )
            ''')

            # Command history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    success BOOLEAN,
                    timestamp TEXT,
                    session_id TEXT,
                    context TEXT
                )
            ''')
            conn.commit()

    def _load_quick_memory(self) -> Dict[str, Any]:
        """Load quick access memory from JSON"""
        if self.quick_memory_path.exists():
            try:
                with open(self.quick_memory_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        return {
            'frequent_commands': {},
            'user_patterns': {},
            'system_shortcuts': {},
            'learned_preferences': {}
        }

    def _save_quick_memory(self):
        """Save quick access memory to JSON"""
        try:
            with open(self.quick_memory_path, 'w') as f:
                json.dump(self.quick_memory, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save quick memory: {e}")

    def store_conversation(self, user_request: str, agent_response: Dict[str, Any],
                          execution_results: List[Dict[str, Any]], system_state: Dict[str, Any]):
        """Store conversation in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations
                    (session_id, timestamp, user_request, agent_response, execution_results, system_state)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id,
                    datetime.now().isoformat(),
                    user_request,
                    json.dumps(agent_response),
                    json.dumps(execution_results),
                    json.dumps(system_state)
                ))
                conn.commit()
        except Exception as e:
            print(f"Warning: Could not store conversation: {e}")

    def store_command_history(self, command: str, success: bool, context: str = ""):
        """Store command execution history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO command_history (command, success, timestamp, session_id, context)
                    VALUES (?, ?, ?, ?, ?)
                ''', (command, success, datetime.now().isoformat(), self.session_id, context))
                conn.commit()

            # Update quick memory for frequent commands
            cmd_key = command.split()[0] if command.split() else command
            if cmd_key in self.quick_memory['frequent_commands']:
                self.quick_memory['frequent_commands'][cmd_key] += 1
            else:
                self.quick_memory['frequent_commands'][cmd_key] = 1

        except Exception as e:
            print(f"Warning: Could not store command history: {e}")

    def store_system_fact(self, fact_key: str, fact_value: str):
        """Store learned system fact"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO system_facts (fact_key, fact_value, timestamp, session_id)
                    VALUES (?, ?, ?, ?)
                ''', (fact_key, fact_value, datetime.now().isoformat(), self.session_id))
                conn.commit()
        except Exception as e:
            print(f"Warning: Could not store system fact: {e}")

    def get_recent_conversations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent conversations for context"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_request, agent_response, timestamp
                    FROM conversations
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))

                conversations = []
                for row in cursor.fetchall():
                    try:
                        conversations.append({
                            'user_request': row[0],
                            'agent_response': json.loads(row[1]),
                            'timestamp': row[2]
                        })
                    except json.JSONDecodeError:
                        continue

                return conversations
        except Exception as e:
            print(f"Warning: Could not retrieve conversations: {e}")
            return []

    def get_command_patterns(self) -> Dict[str, Any]:
        """Get command usage patterns"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT command, COUNT(*) as frequency,
                           AVG(CASE WHEN success THEN 1 ELSE 0 END) as success_rate
                    FROM command_history
                    GROUP BY command
                    ORDER BY frequency DESC
                    LIMIT 10
                ''')

                patterns = {}
                for row in cursor.fetchall():
                    patterns[row[0]] = {
                        'frequency': row[1],
                        'success_rate': row[2]
                    }
                return patterns
        except Exception as e:
            print(f"Warning: Could not retrieve command patterns: {e}")
            return {}

    def get_system_facts(self) -> Dict[str, str]:
        """Get stored system facts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT fact_key, fact_value FROM system_facts')
                return {row[0]: row[1] for row in cursor.fetchall()}
        except Exception as e:
            print(f"Warning: Could not retrieve system facts: {e}")
            return {}

    def get_memory_context(self) -> str:
        """Generate memory context for Gemini"""
        recent_conversations = self.get_recent_conversations(3)
        command_patterns = self.get_command_patterns()
        system_facts = self.get_system_facts()

        context = "\n=== MEMORY CONTEXT ===\n"

        # Recent conversations
        if recent_conversations:
            context += "Recent Conversations:\n"
            for conv in recent_conversations:
                # Limit the length of the agent response in memory context to avoid prompt stuffing
                agent_response_snippet = conv['agent_response'].get('user_message', conv['agent_response'].get('explanation', 'N/A'))
                context += f"- User: {conv['user_request'][:100]}...\n"
                context += f"  Agent: {agent_response_snippet[:100]}...\n"
                context += f"  Time: {conv['timestamp']}\n"

        # Command patterns
        if command_patterns:
            context += "\nFrequent Commands:\n"
            for cmd, stats in list(command_patterns.items())[:5]:
                context += f"- {cmd}: used {stats['frequency']} times (success: {stats['success_rate']:.1%})\n"

        # System facts
        if system_facts:
            context += "\nLearned System Facts:\n"
            for key, value in list(system_facts.items())[:5]:
                context += f"- {key}: {value}\n"

        # Quick memory insights
        if self.quick_memory['learned_preferences']:
            context += "\nUser Preferences:\n"
            for pref, value in self.quick_memory['learned_preferences'].items():
                context += f"- {pref}: {value}\n"

        context += "=== END MEMORY CONTEXT ===\n"
        return context

    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old memory data"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
            cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM conversations WHERE timestamp < ?', (cutoff_iso,))
                cursor.execute('DELETE FROM command_history WHERE timestamp < ?', (cutoff_iso,))
                conn.commit()

            print(f"Cleaned up memory data older than {days_to_keep} days")
        except Exception as e:
            print(f"Warning: Could not cleanup old data: {e}")

class OSAgent:
    def __init__(self, gemini_api_key: str):
        """Initialize the OS Agent with Gemini API key and memory"""
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_linux = self.system == 'linux'

        # Configure Gemini for OS Agent
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Keep 1.5 Flash for OS interactions

        # Initialize memory manager
        self.memory = MemoryManager()

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # System information
        self.system_info = self._get_system_info()
        self.logger.info(f"OS Agent initialized on {self.system_info['system']} {self.system_info['version']}")

        # Store system info as facts
        self.memory.store_system_fact("os_system", self.system_info['system'])
        self.memory.store_system_fact("os_version", self.system_info['version'])
        self.memory.store_system_fact("hostname", self.system_info['hostname'])

        # Browser automation setup removed

    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            return {
                'system': platform.system(),
                'version': platform.version(),
                'release': platform.release(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'hostname': platform.node(),
                'username': os.getenv('USERNAME' if self.is_windows else 'USER'),
                'home_dir': str(Path.home()),
                'current_dir': os.getcwd(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'disk_usage': {
                    'total': psutil.disk_usage('/').total if not self.is_windows else psutil.disk_usage('C:').total,
                    'used': psutil.disk_usage('/').used if not self.is_windows else psutil.disk_usage('C:').used,
                    'free': psutil.disk_usage('/').free if not self.is_windows else psutil.disk_usage('C:').free
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}

    def _execute_command(self, command: str, shell: bool = True, capture_output: bool = True, confirm: bool = False) -> Dict[str, Any]:
        """
        Execute a system command.
        This method no longer blocks dangerous commands by itself.
        The `confirm` parameter is now used to indicate if the command was
        pre-approved by the user on the frontend.
        """
        if not confirm:
            self.logger.warning(f"Attempted to execute command '{command}' without explicit confirmation. Blocking as a safeguard.")
            result = {
                'success': False,
                'error': 'Command requires explicit confirmation from user.',
                'output': '',
                'command': command
            }
            self.memory.store_command_history(command, False, "no_confirmation_received")
            return result

        try:
            self.logger.info(f"Executing command: {command}")

            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture_output,
                text=True,
                timeout=60 # Increased timeout slightly for more complex commands
            )

            exec_result = {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'output': result.stdout.strip() if result.stdout else '',
                'error': result.stderr.strip() if result.stderr else '',
                'command': command
            }

            # Store in memory
            self.memory.store_command_history(command, exec_result['success'])

            return exec_result

        except subprocess.TimeoutExpired:
            result = {
                'success': False,
                'error': 'Command timed out (60s limit)',
                'output': '',
                'command': command
            }
            self.memory.store_command_history(command, False, "timeout")
            return result
        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'output': '',
                'command': command
            }
            self.memory.store_command_history(command, False, f"exception: {str(e)}")
            return result

    def _get_context_prompt(self) -> str:
        """Generate context prompt for Gemini based on system info and memory"""
        memory_gb = self.system_info['memory_total'] / (1024**3)
        disk_free_gb = self.system_info['disk_usage']['free'] / (1024**3)

        # Get memory context
        memory_context = self.memory.get_memory_context()

        return f"""
You are an AI OS agent running on {self.system_info['system']} {self.system_info['release']}.
System Details:
- Architecture: {self.system_info['architecture']}
- CPU Cores: {self.system_info['cpu_count']}
- Memory: {memory_gb:.1f} GB
- Free Disk Space: {disk_free_gb:.1f} GB
- Current Directory: {self.system_info['current_dir']}
- User: {self.system_info['username']}
- Current Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{memory_context}

Your primary goal is to perform OS operations based on user requests.

For commands that involve **deleting files/directories, formatting disks, changing critical system permissions (e.g., chmod 777), or shutting down/rebooting the system**, you **MUST** set `requires_confirmation: true` for that specific command in the JSON. For all other commands, set it to `false`.
If a command involves moving files or renaming, usually it does not require confirmation unless the destination path would overwrite existing critical system files, or if it's a critical system directory. If in doubt, err on the side of caution and ask for confirmation.

Provide a concise `user_message` that explains what you are doing in simple terms for a non-developer. This message should be short and directly understandable.

Response format should be JSON with the following structure:
{{
    "action_type": "command|info|file_operation|process_management|system_query",
    "commands": [
        {{"command": "command_string_1", "requires_confirmation": true}},
        {{"command": "command_string_2", "requires_confirmation": false}}
    ],
    "user_message": "A short, simple, user-friendly message explaining the action or information provided.",
    "learned_info": "Any new critical information or preference learned from the interaction that should be stored."
}}

Remember:
- For Windows, use Windows-specific commands (dir, type, etc.)
- For Linux, use Linux-specific commands (ls, cat, etc.)
- Always prioritize safety, but enable user confirmation for risky actions.
- Provide clear, simple `user_message`.
- Learn from user patterns and preferences.
- Use memory context to provide better responses.
"""

    async def process_request(self, user_request: str, confirmed_commands: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process user request using Gemini and execute appropriate actions.
        `confirmed_commands` is a list of commands the user has explicitly confirmed.
        """
        if confirmed_commands is None:
            confirmed_commands = []

        try:
            # Prepare the prompt for Gemini
            system_prompt = self._get_context_prompt()

            full_prompt = f"""
{system_prompt}

User Request: {user_request}

Analyze this request and determine what OS operations needs to be performed.
Consider the memory context and previous interactions when formulating your response.
If commands need to be executed, provide them in a structured format.
If it's informational, provide the information directly.

For any command that might be destructive (e.g., deleting files, formatting, changing critical permissions, shutdown/reboot), set "requires_confirmation": true for that command in the JSON. Otherwise, set it to false. If a command involves moving files or renaming, usually it does not require confirmation unless the destination path would overwrite existing critical system files, or if it's a critical system directory. If in doubt, err on the side of caution and ask for confirmation.

Response format should be JSON with the following structure:
{{
    "action_type": "command|info|file_operation|process_management|system_query",
    "commands": [
        {{"command": "command_string_1", "requires_confirmation": true}},
        {{"command": "command_string_2", "requires_confirmation": false}}
    ],
    "user_message": "A short, simple, user-friendly message explaining the action or information provided.",
    "learned_info": "Any new critical information or preference learned from the interaction that should be stored."
}}
"""

            # Get Gemini's analysis
            response = self.model.generate_content(full_prompt)

            try:
                # Try to parse as JSON
                gemini_response = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            except json.JSONDecodeError:
                # If not JSON, treat as plain text and log the malformed response
                self.logger.warning(f"Gemini returned non-JSON response: {response.text.strip()}")
                gemini_response = {
                    "action_type": "info",
                    "commands": [],
                    "user_message": f"I couldn't fully understand that. Gemini provided a non-standard response: {response.text.strip()}",
                    "learned_info": ""
                }

            result = {
                'request': user_request,
                'gemini_response': gemini_response,
                'timestamp': datetime.now().isoformat(),
                'system': self.system_info['system'],
                'execution_results': [],
                'pending_confirmation_commands': []
            }

            # Execute commands if any, checking for confirmation
            if gemini_response.get('commands'):
                for cmd_obj in gemini_response['commands']:
                    command = cmd_obj.get('command', '')
                    requires_confirmation = cmd_obj.get('requires_confirmation', False)

                    if not command.strip():
                        continue

                    if requires_confirmation and command not in confirmed_commands:
                        # If confirmation is required and not yet confirmed, add to pending list
                        result['pending_confirmation_commands'].append(command)
                        self.logger.info(f"Command '{command}' requires confirmation.")
                        continue # Skip execution for now

                    # Execute confirmed or non-confirming commands
                    exec_raw_result = self._execute_command(command, confirm=True)
                    # Streamline execution result for frontend
                    exec_result_for_frontend = {
                        'command': command,
                        'success': exec_raw_result['success'],
                        'output_message': exec_raw_result['output'] if exec_raw_result['success'] else exec_raw_result['error']
                    }
                    result['execution_results'].append(exec_result_for_frontend)

                    # Add a small delay between commands
                    time.sleep(0.1)

            # Browser automation handling removed

            # Store learned information
            if gemini_response.get('learned_info'):
                self.memory.store_system_fact(
                    f"learned_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    gemini_response['learned_info']
                )

            # Store conversation in memory
            current_system_state = self.get_system_status()
            self.memory.store_conversation(
                user_request,
                gemini_response,
                result['execution_results'],
                current_system_state
            )

            # Save quick memory
            self.memory._save_quick_memory()

            return result

        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {
                'error': str(e),
                'request': user_request,
                'timestamp': datetime.now().isoformat(),
                'user_message': f"An internal error occurred: {e}. Please try again.",
                'gemini_response': {}
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/' if not self.is_windows else 'C:')

            # Get running processes count
            process_count = len(psutil.pids())

            # Get network interfaces
            network_interfaces = []
            for interface, addresses in psutil.net_if_addrs().items():
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        network_interfaces.append({
                            'interface': interface,
                            'ip': addr.address
                        })

            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percentage': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percentage': (disk.used / disk.total) * 100
                },
                'processes': process_count,
                'network_interfaces': network_interfaces,
                'uptime': time.time() - psutil.boot_time()
            }

        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}

    def list_processes(self, filter_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """List running processes with optional filtering"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if filter_name is None or filter_name.lower() in pinfo['name'].lower():
                        processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]

        except Exception as e:
            self.logger.error(f"Error listing processes: {e}")
            return []

    def manage_file_operations(self, operation: str, source: str, destination: str = None) -> Dict[str, Any]:
        """Perform file operations safely"""
        try:
            source_path = Path(source)

            if operation == 'copy' and destination:
                dest_path = Path(destination)
                shutil.copy2(source_path, dest_path)
                return {'success': True, 'message': f'Copied {source} to {destination}'}

            elif operation == 'move' and destination:
                dest_path = Path(destination)
                shutil.move(source_path, dest_path)
                return {'success': True, 'message': f'Moved {source} to {destination}'}

            elif operation == 'delete':
                if source_path.is_file():
                    source_path.unlink()
                    return {'success': True, 'message': f'Deleted file {source}'}
                elif source_path.is_dir():
                    shutil.rmtree(source_path)
                    return {'success': True, 'message': f'Deleted directory {source}'}

            elif operation == 'create_dir':
                source_path.mkdir(parents=True, exist_ok=True)
                return {'success': True, 'message': f'Created directory {source}'}

            elif operation == 'info':
                if source_path.exists():
                    stat = source_path.stat()
                    return {
                        'success': True,
                        'info': {
                            'path': str(source_path),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'is_file': source_path.is_file(),
                            'is_directory': source_path.is_dir()
                        }
                    }
                else:
                    return {'success': False, 'error': 'Path does not exist'}

            return {'success': False, 'error': 'Invalid operation'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            conversations = len(self.memory.get_recent_conversations(1000))
            command_patterns = self.memory.get_command_patterns()
            system_facts = len(self.memory.get_system_facts())

            return {
                'total_conversations': conversations,
                'total_system_facts': system_facts,
                'top_commands': list(command_patterns.keys())[:5],
                'memory_location': str(self.memory.memory_dir),
                'session_id': self.memory.session_id
            }
        except Exception as e:
            return {'error': str(e)}

    async def main(self):
        """Main loop for the OS Agent"""
        print(f"OS Agent running on {self.system.upper()}")
        print("Type 'exit' to quit.")
        print("Type 'status' for system status.")
        print("Type 'processes' to list running processes.")
        print("Type 'memory_stats' for agent memory statistics.")
        print("Type 'cleanup_memory' to clean up old memory data.")

        while True:
            try:
                user_input = input("\nOS Agent> ").strip()
                if user_input.lower() == 'exit':
                    print("Exiting OS Agent. Goodbye!")
                    self.memory._save_quick_memory() # Ensure quick memory is saved on exit
                    break
                elif user_input.lower() == 'status':
                    status = self.get_system_status()
                    print(json.dumps(status, indent=2))
                elif user_input.lower() == 'processes':
                    processes = self.list_processes()
                    print(json.dumps(processes, indent=2))
                elif user_input.lower() == 'memory_stats':
                    mem_stats = self.get_memory_stats()
                    print(json.dumps(mem_stats, indent=2))
                elif user_input.lower() == 'cleanup_memory':
                    days = input("Enter number of days of data to keep (e.g., 30): ").strip()
                    try:
                        days_to_keep = int(days)
                        self.memory.cleanup_old_data(days_to_keep)
                        print(f"Memory cleaned. Data older than {days_to_keep} days removed.")
                    except ValueError:
                        print("Invalid number of days. Please enter an integer.")
                else:
                    # Process the request with Gemini
                    response = await self.process_request(user_input)

                    if response.get('pending_confirmation_commands'):
                        print("\n--- ACTION REQUIRED: COMMANDS PENDING CONFIRMATION ---")
                        print("The following commands require your explicit approval before execution:")
                        for cmd in response['pending_confirmation_commands']:
                            print(f"- {cmd}")
                        confirm = input("Do you want to execute these commands? (yes/no): ").strip().lower()
                        if confirm == 'yes':
                            # Re-process with confirmed commands
                            final_response = await self.process_request(user_input, confirmed_commands=response['pending_confirmation_commands'])
                            print("\n--- Agent Response ---")
                            print(f"User Message: {final_response.get('gemini_response', {}).get('user_message', 'No specific message.')}")
                            if final_response.get('execution_results'):
                                print("\nExecution Results:")
                                for exec_res in final_response['execution_results']:
                                    print(f"  Command: {exec_res.get('command', 'N/A')}")
                                    print(f"  Success: {exec_res.get('success', 'N/A')}")
                                    print(f"  Output: {exec_res.get('output_message', 'N/A')}\n")
                            if final_response.get('error'):
                                print(f"Error: {final_response['error']}")
                        else:
                            print("Commands not confirmed. Action aborted.")
                    else:
                        print("\n--- Agent Response ---")
                        print(f"User Message: {response.get('gemini_response', {}).get('user_message', 'No specific message.')}")

                        if response.get('execution_results'):
                            print("\nExecution Results:")
                            for exec_res in response['execution_results']:
                                # Removed specific browser automation handling here
                                print(f"  Command: {exec_res.get('command', 'N/A')}")
                                print(f"  Success: {exec_res.get('success', 'N/A')}")
                                print(f"  Output: {exec_res.get('output_message', 'N/A')}\n")
                        if response.get('error'):
                            print(f"Error: {response['error']}")


            except Exception as e:
                self.logger.error(f"Unhandled error in main loop: {e}")
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Get API key from environment variable
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    agent = OSAgent(gemini_api_key=GEMINI_API_KEY)
    asyncio.run(agent.main())