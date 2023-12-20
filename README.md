### README for the ECE 4880 Project 1 Repository

#### Repository Overview
The [ECE 4880 Project 1]([https://github.com/SamNicklez/ece4880project1](https://github.com/SamNicklez/thermometer-app)) repository is a project that implements a thermometer with a web interface. It is a combination of a server-side Python application and a client-side Vue.js application.

#### Project Description
This project is designed to provide temperature readings through a web interface. It consists of two main parts: a server application written in Python and a client application developed using Vue.js.

#### Key Features
- **Thermometer Functionality**: The project includes Python scripts to interface with a thermometer sensor.
- **Web Interface**: A Vue.js client application displays temperature data in real-time.
- **Text Messaging Alerts**: The server can send text message alerts based on temperature readings.
- **Graphical Display of Data**: The client application includes a graphical representation of temperature data.

#### Getting Started
1. **Server Setup**:
   - The server application (`Server/main.py`) interfaces with the thermometer and provides an API for the client.
   - It includes scripts like `lcd.py` for LCD display, `pi.py` for Raspberry Pi functionalities, `textMessage.py` for sending SMS alerts, and `thermometer.py` for thermometer interfacing.

2. **Client Application**:
   - The client (`Client/src/App.vue`) is a Vue.js application that fetches and displays temperature data.
   - It uses components like `HelloWorld.vue`, `TheWelcome.vue`, and `WelcomeItem.vue` for various UI elements.

3. **Deployment**:
   - The project includes a `start_up.sh` script for server deployment.

#### Project Structure
- **Client Application**:
  - Vue.js components and assets (e.g., [`App.vue`](https://github.com/SamNicklez/thermometer-app/blob/main/Client/src/App.vue)).
  - Main JavaScript file (e.g., [`main.js`](https://github.com/SamNicklez/thermometer-app/blob/main/Client/src/main.js)).
- **Server Application**:
  - Python scripts for server logic and sensor interfacing (e.g., [`main.py`](https://github.com/SamNicklez/thermometer-app/blob/main/Server/main.py)).
- **Testing**:
  - Test scripts for API and Raspberry Pi functionalities (e.g., [`test_api.py`](https://github.com/SamNicklez/thermometer-app/blob/main/test/test_api.py)).
