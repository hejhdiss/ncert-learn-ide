#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void RunMainCreator() {
    // Run the maincreator.exe from the current directory
    printf("Running maincreator.exe...\n");
    system("maincreator.exe"); // Assuming maincreator.exe is in the same directory
}

int main() {
    // Inform the user that the process will reset and delete all pip packages
    printf("Warning: This will reset and delete all pip packages installed in the Ncert Learn IDE python environment.\n");
    
    // Ask the user for confirmation to proceed
    char response[10];
    printf("Do you want to continue ? (yes/no): ");
    fgets(response, sizeof(response), stdin);

    // Remove the newline character at the end of the response
    response[strcspn(response, "\n")] = 0;

    // If the user answers 'yes', run the maincreator.exe
    if (strcmp(response, "yes") == 0) {
        RunMainCreator();
    } else {
        printf("Operation cancelled. maincreator.exe was not run.\n");
    }

    return 0;
}
