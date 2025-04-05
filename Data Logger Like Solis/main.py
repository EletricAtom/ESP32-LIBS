# Importing required libraries
import network           # For managing Wi-Fi interfaces (STA/AP)
import utime             # For handling delays (sleep)
import socket            # For socket communication (HTTP server)
import ure               # For regular expressions (not used here)
import urequests         # For sending HTTP requests
import gc                # For garbage collection (memory management)

#--------------------------------------------- Variable Definitions -------------------------------------------------------------
rede_selecionada = ''      # Stores the selected Wi-Fi network
ssid = ''                  # Wi-Fi SSID
password_wifi = ''         # Wi-Fi password

opcoes_html = ""           # HTML options for Wi-Fi list
lista_redes = []           # List of available networks

valor_da_rede = ''         # Holds the chosen Wi-Fi network value

deauth = True              # Used to verify login (default not authenticated)
nome = ''                  # Username
senha = ''                 # Password
pag = False                # Controls the page flow
value = False              # Controls if network selection has already been processed

connected_wifi = False     # Flag to track if Wi-Fi is connected

url = "https://rickandmortyapi.com/api/character/322"  # URL to make API request to

#********************************************** End of Variable Definitions *****************************************************


# Enabling station mode (client) and access point mode
wlan = network.WLAN()
wlan.active(True)

ap = network.WLAN(network.AP_IF)
ap.active(True)

# Configuring the access point (AP) with SSID and password
ap.config(essid="Rede VoltSys", password="123456789", authmode=network.AUTH_WPA_WPA2_PSK)

# Wait for AP to become active
while not ap.active():
    utime.sleep(1)

print('AP active. IP:', ap.ifconfig()[0])

# Create a socket for the HTTP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Server listening at http://%s:80' % ap.ifconfig()[0])

# Scan and print available networks
print(wlan.scan())
print('Available Networks')

# Enumerate and store available SSIDs
for inxdex, redes in enumerate(wlan.scan()):
    print(redes[0].decode('utf8'))
    lista_redes.append(redes[0].decode('utf8'))

#------------------------------------ HTML Pages Definitions -----------------------------------------

# Login Page
pagina_login = f"""\
HTTP/1.1 200 OK
<!DOCTYPE html>
<html>
  <head>
    <title>ESP32</title>
  </head>
  <body style="background: linear-gradient(to right, black, blue);  color: white;  display: flex;  justify-content: center;
  align-items: center;  flex-direction: column;  font-family: 'Segoe UI';">
  <h1>ESP32 DataLogger</h1>
  <form method="POST" style="display: flex; justify-content: center; align-items: center; flex-direction: column; height: 50%; width: 30%;
  border-radius: 20px; background-color: rgba(0,0,255,0.3); backdrop-filter: blur(10px); border: 1px solid white; padding: 20px;
  margin: 20px; gap: 20px;">
    <h2>Digite o usuário:</h2>
    <input style="width: 80%; height: 30px; padding: 2px; border-radius: 5px;" name="nome" type="text"/>
    <h2>Digite a senha:</h2>
    <input style="width: 80%; height: 30px; padding: 2px; border-radius: 5px;" name="senha" type="password" />
    <input style="height: 30px; padding: 2px; width: 40%; border-radius: 5px; margin-top: 20px;" type="submit" value="ENTRAR" />
  </form>

  </body>
</html>
""" 

# Generate the HTML options list from scanned networks
for rede in lista_redes:
    opcoes_html += f'<option value="{rede}">{rede}</option>\n'

# Network Selection Page
pagina_principal = f"""\
HTTP/1.1 200 OK
<!DOCTYPE html>
<html>
  <head>
    <title>ESP32</title>
  </head>
  <body style="background: linear-gradient(to right, black, blue);  color: white;  display: flex;  justify-content: center;
  align-items: center;  flex-direction: column;  font-family: 'Segoe UI';">
    <h1>Selecione a rede WIFI</h1>
  <form style="display: flex;  justify-content: center;  align-items: center;  flex-direction: column;  height: 50%;  width: 30%;  border-radius: 20px;
  background-color: rgba(0,0,255,0.3);  backdrop-filter: blur(10px);  border: 1px solid white;  padding: 20px;  margin: 20px;  gap: 20px;" method='POST'>
      <label for="rede">Escolha uma rede Wi-Fi:</label><br>
          <select name="rede" size="10">
            {opcoes_html}
          </select><br><br>
          <input style="height: 30px; padding: 2px; width: 40%; border-radius: 5px; margin-top: 20px;" type="submit" value="PROXIMO" />
  </form>
  
  </body>
</html>

"""  # (Contains a <select> list for available networks)

# Wi-Fi Authentication Page (asks for Wi-Fi password)
pagina_auth = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
  <head>
    <title>ESP32</title>
  </head>
  <body style="background: linear-gradient(to right, black, blue);  color: white;  display: flex;  justify-content: center;  align-items: center;
  flex-direction: column;  font-family: 'Segoe UI';">
    <h1>Servidor ESP32 ativo!</h1>
    <form style="display: flex;  justify-content: center;  align-items: center;  flex-direction: column;  height: 50%;  width: 30%;  border-radius: 20px;
    background-color: rgba(0,0,255,0.3);  backdrop-filter: blur(10px);  border: 1px solid white;  padding: 20px;  margin: 20px;
    gap: 20px;" method="POST">
      <h2>Digite a senha da rede selecionada</h2>
      <input style="width: 80%; height: 30px; padding: 2px; border-radius: 5px;" name="pass_wifi" type="password" />
      <input style="height: 30px;  padding: 2px;  width: 40%; border-radius: 5px; margin-top: 20px;" type="submit" value="ENVIAR" />
    </form>
  </body>
</html>
"""

# Final Page after successful connection
pagina_end = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<!DOCTYPE html>
<html>
  <head>
    <title>ESP32</title>
    </head>
  <body style="background: linear-gradient(to right, black, blue);  color: white;  display: flex;  justify-content: center;  align-items: center;
  flex-direction: column;  font-family: 'Segoe UI';">
    <h1>Servidor ESP32 ativo!</h1>
  <form style="display: flex;  justify-content: center;  align-items: center;  flex-direction: column;  height: 50%;  width: 30%;  border-radius: 20px;
  background-color: rgba(0,0,255,0.3);  backdrop-filter: blur(10px);  border: 1px solid white;  padding: 20px;  margin: 20px;
  gap: 20px;" method="POST">
    <h2>Rede Conectada com Sucesso!</h2>
  </form>
  
  </body>
</html>
"""

#------------------------------ Main Server Loop ------------------------------

while True:
    cl, addr = s.accept()  # Accept connection
    print('Client connected from', addr)
    request = cl.recv(1024)  # Receive HTTP request
    request_str = request.decode()  # Decode the request
    print('Request:\n', request)

    # Define which page to send
    if deauth and pag == False:
        pagina = pagina_login

    if deauth == False and pag == False:
        pagina = pagina_principal

    # Handle POST requests
    if 'POST' in request_str:
        body = request_str.split('\r\n\r\n')[1]  # Get form data
        print('Body:', body)

        dados = body.split('&')
        dados_dict = {}

        # Parse key-value pairs from form
        for item in dados:
            if '=' in item:
                chave, valor = item.split('=')
                dados_dict[chave] = valor

        # Extract values from the form
        nome = dados_dict.get('nome', '')
        senha = dados_dict.get('senha', '')
        rede_selecionada = dados_dict.get('rede', '')
        ssid = dados_dict.get('ssid', '')
        password_wifi = dados_dict.get('pass_wifi', '')

        # Store selected network only once
        try:
            if (rede_selecionada != '') and (value == False):
                valor_da_rede = rede_selecionada
                value = True
        except Exception as e:
            print("Error saving network:", e)

        print('Selected network:', rede_selecionada)
        print('Username:', nome)
        print('Password:', senha)

        # Send response and close connection
        cl.send(pagina)
        cl.close()
        continue

    # Login verification
    if nome.lower().strip() == "admin" and senha.lower().strip() == "admin":
        deauth = False

    # If a valid network is selected and not yet connected
    if rede_selecionada in lista_redes and (connected_wifi == False):
        pag = True
        pagina = pagina_auth

    # If Wi-Fi is connected, show the final page
    if (pag == True) and (connected_wifi == True):
        pagina = pagina_end

    # Send the chosen page
    cl.send(pagina)
    cl.close()

    # Attempt to connect to the selected Wi-Fi network
    if (pagina == pagina_auth) and (password_wifi != ''):
        print("Connecting to network:", valor_da_rede)
        print("Password provided:", password_wifi)

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)

        try:
            if not sta_if.isconnected():
                print("Trying to connect...")
                sta_if.connect(valor_da_rede.strip(), password_wifi.strip())
                timeout = 20
                while not sta_if.isconnected() and timeout > 0:
                    utime.sleep(1)
                    timeout -= 1
        except Exception as e:
            print("Connection error:", e)

        if sta_if.isconnected():
            print('Connected successfully! IP:', sta_if.ifconfig()[0])
            connected_wifi = True
            gc.collect()
        else:
            utime.sleep(2)
            ap.active(True)  # Reactivate AP if connection fails
            print('Connection failed.')

        # Make HTTPS GET request to external API if connected
        try:
            if connected_wifi == True:
                print('Making GET request to URL:', url)

                gc.collect()  # Free memory

                response = urequests.get(url)
                print('Status:', response.status_code)

                try:
                    print('Response:', response.text)
                except Exception as e:
                    print('Error reading response:', e)

                response.close()
                gc.collect()

        except Exception as erro:
            print('HTTPS request error:', erro)
