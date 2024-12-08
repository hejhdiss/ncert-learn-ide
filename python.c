#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#endif

// Define the maximum command size
#define MAX_COMMAND_SIZE 1024

int main(int argc, char *argv[]) {
    // Check if arguments exceed buffer limit
    if (argc > 1) {
        size_t total_arg_length = 0;
        for (int i = 1; i < argc; i++) {
            total_arg_length += strlen(argv[i]) + 1; // +1 for space or null-terminator
        }

        if (total_arg_length >= MAX_COMMAND_SIZE - 30) { // Account for base command length
            fprintf(stderr, "Error: Command exceeds maximum allowed length.\n");
            return EXIT_FAILURE;
        }
    }

    // Prepare the base PowerShell command
    char command[MAX_COMMAND_SIZE] = "powershell.exe -Command \"& { ./venv/Scripts/python.exe";

    // Append the arguments to the PowerShell command
    for (int i = 1; i < argc; i++) {
        strcat(command, " ");
        strcat(command, argv[i]);
    }

    // Close the PowerShell command
    strcat(command, " }\"");

    // Execute the command and check for success
    int result = system(command);

    if (result != 0) {
        fprintf(stderr, "Error: Command execution failed with code %d.\n", result);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}

