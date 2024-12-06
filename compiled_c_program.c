#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <io.h> // For access() on Windows

int main() {
    FILE *file;
    char gcc_path[256], c_file_path[256], exe_name[256], cmd[512];

    // Read the GCC path from the file
    file = fopen("gccpath.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open gccpath.txt\n");
        return 1;
    }
    fgets(gcc_path, sizeof(gcc_path), file);
    fclose(file);

    // Read the C file path from the file
    file = fopen("inputc.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open inputc.txt\n");
        return 1;
    }
    fgets(c_file_path, sizeof(c_file_path), file);
    fclose(file);

    // Remove newline characters from paths
    gcc_path[strcspn(gcc_path, "\n")] = 0;
    c_file_path[strcspn(c_file_path, "\n")] = 0;

    // Extract the name of the C file (without path and extension)
    char *file_name = strrchr(c_file_path, '\\'); // For Windows
    if (file_name == NULL) {
        file_name = strrchr(c_file_path, '/'); // For Unix-like systems
    }
    file_name = (file_name != NULL) ? file_name + 1 : c_file_path; // Skip the slash if found
    strcpy(exe_name, file_name);
    char *dot = strrchr(exe_name, '.');
    if (dot != NULL) *dot = '\0'; // Remove the file extension

    // Replace backslashes with forward slashes in C file path for consistency
    for (int i = 0; c_file_path[i]; i++) {
        if (c_file_path[i] == '\\') {
            c_file_path[i] = '/';
        }
    }

    // Get the directory of the C file (for output .exe)
    char output_dir[512];
    strcpy(output_dir, c_file_path);
    char *last_slash = strrchr(output_dir, '/');
    if (last_slash != NULL) {
        *last_slash = '\0'; // Remove the file name to get the directory
    }

    // Create the PowerShell command to compile
    snprintf(cmd, sizeof(cmd),
             "powershell -Command \"& '%s' -o '%s/%s.exe' '%s'; pause\"",
             gcc_path,
             output_dir, exe_name,
             c_file_path);

    // Print the command to debug
    printf("Running command: %s\n", cmd);

    // Run the PowerShell command to compile
    int result = system(cmd);
    if (result == 0) {
        printf("Compilation succeeded.\n");
    } else {
        printf("Error: Compilation failed.\n");
        return 1;
    }

    // Check if the compiled executable exists
    char exe_path[512];
    snprintf(exe_path, sizeof(exe_path), "%s/%s.exe", output_dir, exe_name);
    if (access(exe_path, F_OK) != -1) {
        printf("Running the compiled executable: %s\n", exe_path);
        
        // Run the executable using PowerShell
        snprintf(cmd, sizeof(cmd), "powershell -Command \"& '%s'; pause\"",
                 exe_path);
        system(cmd);
    } else {
        printf("Compilation failed or the file does not exist.\n");
    }

    return 0;
}
