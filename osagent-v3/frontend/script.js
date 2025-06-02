document.addEventListener('DOMContentLoaded', () => {
    const terminalInput = document.getElementById('terminal-input');
    const terminalOutput = document.getElementById('terminal-output');
    const terminalBody = document.getElementById('terminal-body');

    let awaitingConfirmation = false;
    let pendingCommandsToConfirm = [];
    let currentCommand = ''; // Store the original command for re-sending

    // Function to append output to the terminal
    function appendOutput(text, className = '') {
        const p = document.createElement('p');
        p.className = className;
        // Handle newlines within the text content
        p.innerHTML = text.replace(/\n/g, '<br>');
        terminalOutput.appendChild(p);
        terminalBody.scrollTop = terminalBody.scrollHeight; // Auto-scroll to bottom
    }

    // Initial welcome message
    appendOutput('Welcome to OS Agent Terminal. Type "help" for commands.', 'info');
    appendOutput('os-agent $ ');

    async function sendCommand(command, confirmedCommands = []) {
        try {
            appendOutput('Processing...', 'info'); // Show processing message immediately
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command, confirmed_commands: confirmedCommands }),
            });

            const data = await response.json();

            if (response.ok) {
                // Display the primary user message
                const userMessage = data.gemini_response?.user_message || "Action processed.";
                appendOutput(userMessage, 'success');

                // Check if confirmation is needed
                if (data.pending_confirmation_commands && data.pending_confirmation_commands.length > 0) {
                    awaitingConfirmation = true;
                    pendingCommandsToConfirm = data.pending_confirmation_commands;
                    appendOutput(`
⚠️ This action involves sensitive operations.
To proceed with these commands:
${pendingCommandsToConfirm.map(cmd => `- "${cmd}"`).join('\n')}
Type 'yes' to confirm and execute, or 'no' to cancel.
                    `, 'warning');
                    appendOutput('Confirm (yes/no): ');
                    terminalInput.focus();
                    return; // Stop processing further until confirmation
                }

                // If no confirmation needed or already confirmed, display execution results concisely
                awaitingConfirmation = false;
                pendingCommandsToConfirm = []; // Clear pending commands

                if (data.execution_results && data.execution_results.length > 0) {
                    data.execution_results.forEach(result => {
                        const statusClass = result.success ? 'success' : 'error';
                        let message = '';

                        // This block now handles all OS command results
                        appendOutput(`Executing: ${result.command}`, 'info');
                        const commandName = result.command.split(' ')[0]; // Just show the first part of command
                        message = `[${commandName}] ${result.output_message || (result.success ? 'Completed.' : 'Failed.')}`;

                        // Enhanced error explanation for failed commands
                        if (!result.success) {
                            let errorSummary = `Error: The command '${commandName}' failed.`;
                            let recommendation = 'Please double-check the command, file paths, or permissions.';

                            if (result.output_message) {
                                // Try to make the error message more user-friendly
                                if (result.output_message.includes('No such file or directory') || result.output_message.includes('No such file or folder')) {
                                    errorSummary = `Error: The file or directory was not found.`;
                                    recommendation = `Ensure the path you provided is correct.`;
                                } else if (result.output_message.includes('Permission denied')) {
                                    errorSummary = `Error: Permission denied.`;
                                    recommendation = `You might not have the necessary permissions. Try running the agent with administrative privileges if appropriate for the task.`;
                                } else if (result.output_message.includes('command not found') || result.output_message.includes('is not recognized as an internal or external command')) {
                                    errorSummary = `Error: Command not found.`;
                                    recommendation = `The command might be misspelled or not installed on your system.`;
                                }
                            }
                            message = `${errorSummary}<br>Details: ${result.output_message}<br>Suggestion: ${recommendation}`;
                        }
                        appendOutput(message, statusClass);
                    });
                } else {
                    // Only show this if no commands were executed at all (e.g., just info response)
                    if (!data.gemini_response?.commands?.length) { // Removed browser_task check
                        appendOutput("No specific execution steps were needed for this request.", 'info');
                    }
                }
            } else {
                appendOutput(`Error from server: ${data.detail || 'Unknown error'}`, 'error');
            }
        } catch (error) {
            appendOutput(`An unexpected error occurred: ${error.message}`, 'error');
            console.error('Fetch error:', error);
        } finally {
            appendOutput('os-agent $ ');
            terminalInput.focus(); // Keep focus on input
        }
    }


    terminalInput.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') {
            const command = terminalInput.value.trim();
            terminalInput.value = ''; // Clear input

            if (command === '') {
                appendOutput('os-agent $ ');
                return;
            }

            // Echo the command back to the terminal
            appendOutput(`os-agent $ ${command}`, 'prompt-echo');

            if (awaitingConfirmation) {
                if (command.toLowerCase() === 'yes') {
                    awaitingConfirmation = false; // Reset flag
                    appendOutput('Confirmation received. Resuming...', 'info');
                    await sendCommand(currentCommand, pendingCommandsToConfirm); // Resend original command with confirmations
                    currentCommand = ''; // Clear stored command
                } else if (command.toLowerCase() === 'no') {
                    appendOutput('Command execution cancelled by user.', 'info');
                    awaitingConfirmation = false;
                    pendingCommandsToConfirm = [];
                    currentCommand = '';
                    appendOutput('os-agent $ ');
                } else {
                    appendOutput("Invalid response. Please type 'yes' or 'no'.", 'error');
                    appendOutput('Confirm (yes/no): ');
                }
                return; // Stop here if awaiting confirmation
            }

            // Handle special frontend-only commands
            if (command.toLowerCase() === 'help') {
                appendOutput(`
Available commands:
- Any natural language OS request (e.g., "list files")
- 'status' - Get system status
- 'processes' - List running processes
- 'info' - Get system information
- 'memory_stats' - Show agent memory statistics
- 'cleanup_memory' - Clean up old memory data
- 'help' - Show this help
- 'clear' - Clear the terminal screen
- 'quit' - Exit the agent (frontend only)
                `, 'info');
                appendOutput('os-agent $ ');
                return;
            } else if (command.toLowerCase() === 'clear') {
                terminalOutput.innerHTML = ''; // Clear content
                appendOutput('os-agent $ ');
                return;
            } else if (command.toLowerCase() === 'quit') {
                appendOutput('Exiting OS Agent. Goodbye!', 'info');
                terminalInput.disabled = true; // Disable input
                return;
            }

            // Store the command before sending, in case confirmation is needed
            currentCommand = command;
            // Send command to backend
            await sendCommand(command);
        }
    });
});