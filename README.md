# 🕵️‍♂️ CheatChat - The Hidden Classroom Chat

This project was originally created as a **hidden chat** used by me and my classmates. It was secretly hosted on our school's cluster **without anyone knowing** \\\_(ò_ò)_/  

Now, you can use it to chat with your friends by hosting your own server and connecting through the client. 💬🚀  

---

## 🚀 How to Host the Server  
To run the chat server, follow these steps:  

1. **Clone the repository**  
    ```sh
    git clone https://github.com/yourusername/cheatchat.git
    cd cheatchat
    ```

1. **Create a virtual environment** (optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows venv\Scripts\activate
   ```

1. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

1. **Start the server** (optional but recommended)
    ```sh
    python src/server/server.py
    ```
    The server will now listen for incoming connections. 🎧

## 💻 How to Start the Client

1. **Run the client application**

    ```sh
    python src/client/client.py
    ```

1. **Enter the server details**
    
    The application will prompt you to enter:
    * **Host** (e.g. `127.0.0.1` for local testing)
    * **Port** (default: `9999`, unless changed)
    * **Username** (Choose your chat name)

1. **Start chatting! 🎉💬**