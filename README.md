# 🛡️ SecureWipe_MicroSD

An advanced secure data wiping utility focused on permanently erasing data from MicroSD cards and removable storage devices. This project is designed to prevent sensitive data recovery by using overwrite-based wiping techniques and secure deletion mechanisms.

Built for cybersecurity learning, digital forensics awareness, and secure storage sanitization practices.

---

# 📦 Technologies

- Python
- File Handling
- Secure Overwrite Algorithms
- OS Module
- Random Data Generation
- Command Line Interface (CLI)
- Storage Device Detection
- Data Sanitization Techniques

---

# ✨ Features

Here’s what you can do with SecureWipe_MicroSD:

- **Secure File Wiping:** Permanently erase files by overwriting their contents multiple times before deletion.

- **MicroSD Card Sanitization:** Wipe entire removable storage devices to reduce the chances of forensic recovery.

- **Multiple Overwrite Passes:** Supports repeated overwrite operations using random patterns and zeros.

- **Storage Detection:** Detects connected removable drives and target storage devices.

- **CLI-Based Interface:** Lightweight and efficient command-line utility for quick execution.

- **Cross-Platform Logic:** Designed with Python to work across multiple operating systems with minimal changes.

- **Progress Monitoring:** Displays wiping progress and status messages during execution.

- **Error Handling:** Prevents accidental crashes during wipe operations and validates device access.

---

# 🔒 Why Secure Wiping Matters

Deleting files normally does not completely erase the data. In many cases, deleted files can still be recovered using forensic recovery tools because only the file references are removed from the system.

SecureWipe_MicroSD solves this problem by overwriting the original data multiple times before deletion, making recovery significantly harder.

This project is useful for:

- Cybersecurity learning
- Digital forensics studies
- Privacy protection
- Secure disposal of storage devices
- Protecting sensitive personal or organizational data

---

# ⚙️ The Process

The project was developed by first understanding how file systems handle deletion internally. Regular deletion only removes pointers to the data blocks, while the actual data often remains intact.

To solve this, the application performs overwrite operations directly on files or storage sectors before removing them from the device.

The wiping workflow includes:

1. Detecting the target file or removable drive.
2. Validating permissions and access rights.
3. Overwriting data blocks with random bytes or patterns.
4. Repeating the overwrite process multiple times.
5. Removing the file system references after sanitization.
6. Verifying successful wipe operations.

The project also focuses on preventing accidental misuse by implementing confirmation steps and validation checks before execution.

---

# 🧠 What I Learned

During the development of this project, I gained practical knowledge in several cybersecurity and system-level concepts.

## 🔹 File System Internals

Learned how operating systems manage file deletion and storage allocation.

## 🔹 Data Recovery Concepts

Understood why deleted files can still be recovered using forensic tools and how secure overwriting helps mitigate this issue.

## 🔹 Python System Programming

Worked with Python modules related to file handling, storage management, and operating system interactions.

## 🔹 Secure Coding Practices

Implemented validation and error handling to reduce risks during destructive operations.

## 🔹 Cybersecurity Awareness

Improved understanding of privacy protection, data sanitization standards, and secure disposal techniques.

---

# 📈 Overall Growth

This project helped improve my logical thinking and understanding of low-level storage operations. It also strengthened my cybersecurity fundamentals by combining theory with practical implementation.

More than just building a utility, this project gave me hands-on exposure to how digital data persists even after deletion and how proper sanitization methods are essential in modern cybersecurity practices.

---

# 🚀 Future Improvements

Here are some features planned for future development:

- Add a graphical user interface (GUI)
- Support advanced wiping standards like DoD 5220.22-M
- Add logging and wipe reports
- Implement drive health monitoring
- Add encryption-based sanitization
- Improve cross-platform compatibility
- Add multi-threaded wiping for faster performance
- Support SSD-aware secure erase techniques
- Add forensic verification reports

---

# 🖥️ Running the Project

To run the project locally, follow these steps:

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/SamsonEnochRepos/SecureWipe_MicroSD.git
```

## 2️⃣ Navigate into the Project Folder

```bash
cd SecureWipe_MicroSD
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run the Application

```bash
python main.py
```

---

# ⚠️ Important Warning

This project performs permanent data deletion operations.

- Always double-check the selected device or file before wiping.
- Lost data may not be recoverable.
- Use this tool responsibly and only on devices you own or are authorized to sanitize.

---

# 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

Feel free to fork the repository, create issues, or submit pull requests.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Developed by **SamsonEnochRepos**
