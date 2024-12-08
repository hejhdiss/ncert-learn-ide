#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <direct.h>

void execute_command(const char *command) {
    char exec_command[1024];
    char current_dir[MAX_PATH];

    // Get the current working directory
    if (_getcwd(current_dir, sizeof(current_dir)) == NULL) {
        printf("Error: Unable to get the current directory.\n");
        return;
    }

    // Check if the command involves Python, pip, gcc, g++, or a venv script
    if (strstr(command, "python") == command) {  // Check if it starts with "python"
        // Construct the full path to python.exe in the "python" folder
        snprintf(exec_command, sizeof(exec_command), "\"%s\\python\\venv\\Scripts\\python.exe\" %s", 
                 current_dir, command + 6); // Skip "python " prefix
    } 
    else if (strstr(command, "pip") == command) {  // Check if it starts with "pip"
        // Construct the full path to pip using python.exe
        snprintf(exec_command, sizeof(exec_command), "\"%s\\python\\venv\\Scripts\\python.exe\" -m pip %s", 
                 current_dir, command + 4); // Skip "pip " prefix
    }
    else if (strstr(command, "gcc") == command || strstr(command, "g++") == command) {  // Check if it starts with "gcc" or "g++"
        // Construct the full path to gcc or g++ in the "gcc/bin" folder
        snprintf(exec_command, sizeof(exec_command), "\"%s\\gcc\\bin\\%s\" %s", 
                 current_dir, command, command + 4); // Skip "gcc " or "g++ " prefix
    } 
    else if (strstr(command, "venv") == command) {  // Check if it starts with "venv"
        // Construct the full path to a script in the venv Scripts directory
        snprintf(exec_command, sizeof(exec_command), "\"%s\\python\\venv\\Scripts\\%s\"", 
                 current_dir, command + 5); // Skip "venv " prefix
    }
    else {
        // Block any other command and show an error
        printf("Error: Invalid command. Only 'python', 'pip', 'gcc' and its associates, 'g++' and its associates, and 'venv' commands are allowed.\n");
        return;
    }

    // Execute the command in PowerShell
    int result = system(exec_command);
    if (result != 0) {
        printf("Error: Command execution failed. Make sure the paths to the executables are correct.\n");
    }
}

int main() {
    char command[512];

    printf("Ncert Learn IDE > ");
    while (1) {
        // Get input from the user
        fgets(command, sizeof(command), stdin);

        // Remove the newline character at the end of the command
        command[strcspn(command, "\n")] = 0;

        // Exit if the command is "exit"
        if (strcmp(command, "exit") == 0) {
            break;
        }

        // Execute the command
        execute_command(command);
        printf("\nNcert Learn IDE > ");
    }

    return 0;
}