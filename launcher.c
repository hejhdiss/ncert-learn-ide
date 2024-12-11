#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <windows.h>

int main() {
    // Get the path to the current executable
    char exe_path[MAX_PATH];
    if (GetModuleFileName(NULL, exe_path, sizeof(exe_path)) == 0) {
        printf("Error getting executable path\n");
        return 1;
    }

    // Remove the executable name from the path to get the directory
    char *last_backslash = strrchr(exe_path, '\\');
    if (last_backslash != NULL) {
        *last_backslash = '\0';
    }

    // Construct the paths to Python executable and script (assuming they are in the same directory)
    char python_path[MAX_PATH];
    char script_path[MAX_PATH];

    snprintf(python_path, sizeof(python_path), "%s\\runner\\python.exe", exe_path); // Assuming python.exe is in the same folder
    snprintf(script_path, sizeof(script_path), "%s\\ncert_learn_ide.py", exe_path); // Assuming ncert_learn_ide.py is in the same folder

    // Prepare the command to run
    char command[1024];
    snprintf(command, sizeof(command), "\"%s\" \"%s\"", python_path, script_path);

    // Execute the command
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    // Create the process to run the command
    if (CreateProcess(
            NULL,         // No module name (use command line)
            command,      // Command line
            NULL,         // Process security attributes
            NULL,         // Primary thread security attributes
            FALSE,        // Inherit handles
            CREATE_NO_WINDOW, // Hide the window
            NULL,         // Use parent's environment
            NULL,         // Use parent's current directory
            &si,          // Startup information
            &pi           // Process information
    )) {
        // Wait for 10 seconds before closing the terminal
        Sleep(0); // Sleep for 10 seconds

        // Close process and thread handles
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    } else {
        printf("Error: Unable to create process. Error code: %lu\n", GetLastError());
    }

    // Ensure the terminal closes after 10 seconds
    exit(0);
}


