#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void printStubInformation() {
    printf("Chat Program Started\n");
}

int getLineFromStdin(char *buffer) {
    if (fgets(buffer, 300, stdin) != NULL) {
        // Remove newline if present
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') {
            buffer[len-1] = '\0';
        }
        return 1;
    }
    return 0;
}

// Simple credential check
int check_credentials(const char* id, const char* pw) {
    return ( (strcmp(id, "user1") == 0 && strcmp(pw, "pass1") == 0) ||
             (strcmp(id, "user2") == 0 && strcmp(pw, "pass2") == 0) );
}

int main(int argc, char *argv[])
{
    char cmd[300];
    char id[300];
    char pw[300];

    printStubInformation();
    fflush(stdout);

    while (1)
    {
        printf("command(h for help)>");
        fflush(stdout);

        memset(cmd, 0, sizeof(cmd));
        if (getLineFromStdin(cmd) == 0)
            continue;
        
        if (!strcmp("quit", cmd) || !strcmp("q", cmd))
        {
            //quit
            printf("quit\n");
            fflush(stdout);
            return 0;
        }
        else if (!strcmp("login", cmd) || !strcmp("i", cmd))
        {
            //login
            printf("ID:\n");
            fflush(stdout);
            if (!getLineFromStdin(id)) continue;
            printf("Password:\n");
            fflush(stdout);
            if (!getLineFromStdin(pw)) continue;
            if (check_credentials(id, pw)) {
                printf("login complete\n");
            } else {
                printf("login failed\n");
            }
            fflush(stdout);
        }
        else if (!strcmp("logout", cmd) || !strcmp("t", cmd))
        {
            //logout
            printf("logout\n");
            fflush(stdout);
            printf("logout complete\n");
            fflush(stdout);
        }
        else if (!strcmp("send", cmd) || !strcmp("s", cmd))
        {
            //send message
            printf("send\n");
            fflush(stdout);
            printf("send complete\n");
            fflush(stdout);
        }
        else if (!strcmp("help", cmd) || !strcmp("h", cmd))
        {
            //help
            printf("i: login\n");
            printf("t: logout\n");
            printf("s: send message\n");
            printf("r: receive message\n");
            printf("l: list message\n");
            printf("c: change nickname\n");
            printf("q: quit\n");
            fflush(stdout);
        }
        else
        {
            printf("Bad command\n");
            fflush(stdout);
        }
    }

    return 0;
}