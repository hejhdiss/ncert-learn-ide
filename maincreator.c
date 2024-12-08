#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

void CopyFilesAndDirectories(const char *src, const char *dst) {
    // Declare WIN32_FIND_DATA structure
    WIN32_FIND_DATA findFileData;
    HANDLE hFind = INVALID_HANDLE_VALUE;

    // Add backslash to the source path if necessary
    char srcDir[512], dstDir[512];
    snprintf(srcDir, sizeof(srcDir), "%s\\*", src);  // Add * to search all files and directories in the source
    snprintf(dstDir, sizeof(dstDir), "%s", dst);     // Destination path

    // Open the source directory
    hFind = FindFirstFile(srcDir, &findFileData);
    if (hFind == INVALID_HANDLE_VALUE) {
        printf("Error opening directory %s\n", src);
        return;
    }

    // Loop through the files and directories in the source folder
    do {
        const char *fileName = findFileData.cFileName;

        // Skip "." and ".."
        if (strcmp(fileName, ".") == 0 || strcmp(fileName, "..") == 0) {
            continue;
        }

        // Construct the full paths for the source and destination
        char srcPath[512], dstPath[512];
        snprintf(srcPath, sizeof(srcPath), "%s\\%s", src, fileName);
        snprintf(dstPath, sizeof(dstPath), "%s\\%s", dst, fileName);

        // If it's a directory, create the directory at the destination
        if (findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            CreateDirectory(dstPath, NULL);  // Create the directory in the destination
            CopyFilesAndDirectories(srcPath, dstPath); // Recursively copy contents
        } else {
            // If it's a file, copy it to the destination
            if (CopyFile(srcPath, dstPath, FALSE)) {
                printf("Copied file: %s\n", fileName);
            } else {
                printf("Error copying file: %s\n", fileName);
            }
        }
    } while (FindNextFile(hFind, &findFileData));

    FindClose(hFind); // Close the directory handle
}

int main() {
    // Define the relative paths
    const char *python_exe = "runner\\python.exe";  // Path to python.exe in the 'runner' folder
    const char *venv_dir = "python\\venv";           // Path to the directory where the virtual environment will be created

    // Construct the command to create the virtual environment
    char command[512];
    snprintf(command, sizeof(command), "\"%s\" -m venv \"%s\" --copies", python_exe, venv_dir);

    // Print the command for debugging
    printf("Running command: %s\n", command);

    // Use CreateProcess to execute the command
    STARTUPINFO si = { sizeof(STARTUPINFO) };
    PROCESS_INFORMATION pi;

    if (CreateProcess(
            NULL,            // Application name
            command,         // Command line (constructed)
            NULL,            // Process security attributes
            NULL,            // Thread security attributes
            FALSE,           // Inherit handles
            0,               // Creation flags
            NULL,            // Environment
            NULL,            // Current directory
            &si,             // Startup info
            &pi              // Process information
    )) {
        // Wait for the process to finish
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        printf("Virtual environment created successfully!\n");

        // Copy files and directories from contents\\1 and contents\\2\\Lib to python\\venv
        CopyFilesAndDirectories("contents\\1", "python\\venv");
        CopyFilesAndDirectories("contents\\2\\Lib", "python\\venv\\Lib");

    } else {
        printf("Error: Unable to create virtual environment.\n");
    }

    return 0;
}

