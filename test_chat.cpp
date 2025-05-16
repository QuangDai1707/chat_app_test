#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <vector>
#include <string>
#include <cstring>
#include <sstream>
#include <poll.h>
#include <signal.h>

#define READ_END 0
#define WRITE_END 1

class ChatProcess {
public:
    pid_t pid;
    int to_child[2];   // Parent writes to child
    int from_child[2]; // Parent reads from child

    ChatProcess(const char* program) {
        pipe(to_child);
        pipe(from_child);

        pid = fork();
        if (pid == 0) {
            // Child process
            dup2(to_child[READ_END], STDIN_FILENO);
            dup2(from_child[WRITE_END], STDOUT_FILENO);
            close(to_child[WRITE_END]);
            close(from_child[READ_END]);
            execl(program, program, nullptr);
            perror("execl failed");
            exit(1);
        } else {
            // Parent process
            close(to_child[READ_END]);
            close(from_child[WRITE_END]);
            // Set non-blocking read
            int flags = fcntl(from_child[READ_END], F_GETFL, 0);
            fcntl(from_child[READ_END], F_SETFL, flags | O_NONBLOCK);
        }
    }

    void send_command(const std::string& cmd) {
        std::string to_send = cmd + "\n";
        write(to_child[WRITE_END], to_send.c_str(), to_send.size());
    }

    // Wait for a specific output string, returns the full output seen
    std::string wait_for_output(const std::string& expected) {
        std::string buffer;
        char temp[256];
        while (true) {
            struct pollfd pfd = {from_child[READ_END], POLLIN, 0};
            int ret = poll(&pfd, 1, 10000); // 10s timeout
            if (ret > 0 && (pfd.revents & POLLIN)) {
                ssize_t n = read(from_child[READ_END], temp, sizeof(temp) - 1);
                if (n > 0) {
                    temp[n] = '\0';
                    buffer += temp;
                    std::cout << "Output: " << temp;
                    if (buffer.find(expected) != std::string::npos)
                        break;
                }
            }
        }
        return buffer;
    }

    void terminate() {
        kill(pid, SIGTERM);
        waitpid(pid, nullptr, 0);
        close(to_child[WRITE_END]);
        close(from_child[READ_END]);
    }
};

int main() {
    std::cout << "Starting C++ test sequence..." << std::endl;

    ChatProcess user1("./chat_program");
    ChatProcess user2("./chat_program");

    // Wait for initial prompt
    user1.wait_for_output("command(h for help)>");
    user2.wait_for_output("command(h for help)>");

    // User 1 login
    std::cout << "\nUser 1 logging in..." << std::endl;
    user1.send_command("login");
    user1.wait_for_output("login complete");

    // User 2 login
    std::cout << "\nUser 2 logging in..." << std::endl;
    user2.send_command("login");
    user2.wait_for_output("login complete");

    // User 1 sends message
    std::cout << "\nUser 1 sending message..." << std::endl;
    user1.send_command("send");
    user1.wait_for_output("send complete");
    user1.send_command("Hello from User 1!");

    // User 2 sends message
    std::cout << "\nUser 2 sending message..." << std::endl;
    user2.send_command("send");
    user2.wait_for_output("send complete");
    user2.send_command("Hello from User 2!");

    // User 1 logout
    std::cout << "\nUser 1 logging out..." << std::endl;
    user1.send_command("logout");
    user1.wait_for_output("logout complete");

    // User 2 logout
    std::cout << "\nUser 2 logging out..." << std::endl;
    user2.send_command("logout");
    user2.wait_for_output("logout complete");

    // Quit both programs
    user1.send_command("quit");
    user2.send_command("quit");

    user1.terminate();
    user2.terminate();

    std::cout << "\nC++ Test sequence completed successfully!" << std::endl;
    return 0;
} 