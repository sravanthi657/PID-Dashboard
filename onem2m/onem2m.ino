//#include <JSONVar.h>
//#include <JSON.h>
#include <ArduinoJson.h>
//#include <Arduino.h>
///#include <HTTPClient.h>
#include <time.h>
#include <WiFiClientSecure.h>


uint32_t delayMS;
  
// ##################### Update the Wifi SSID, Password and IP adress of the server ##########
// WIFI params
char* WIFI_SSID = "Mahitha";
char* WIFI_PSWD = "mahi151619";


const char*  server = "esw-onem2m.iiit.ac.in";  // Server URL

const char* test_root_ca= \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDdTCCAl2gAwIBAgILBAAAAAABFUtaw5QwDQYJKoZIhvcNAQEFBQAwVzELMAkG\n" \ 
"A1UEBhMCQkUxGTAXBgNVBAoTEEdsb2JhbFNpZ24gbnYtc2ExEDAOBgNVBAsTB1Jv\n" \
"b3QgQ0ExGzAZBgNVBAMTEkdsb2JhbFNpZ24gUm9vdCBDQTAeFw05ODA5MDExMjAw\n" \
"MDBaFw0yODAxMjgxMjAwMDBaMFcxCzAJBgNVBAYTAkJFMRkwFwYDVQQKExBHbG9i\n" \ 
"YWxTaWduIG52LXNhMRAwDgYDVQQLEwdSb290IENBMRswGQYDVQQDExJHbG9iYWxT\n" \
"aWduIFJvb3QgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDaDuaZ\n" \
"jc6j40+Kfvvxi4Mla+pIH/EqsLmVEQS98GPR4mdmzxzdzxtIK+6NiY6arymAZavp\n" \
"xy0Sy6scTHAHoT0KMM0VjU/43dSMUBUc71DuxC73/OlS8pF94G3VNTCOXkNz8kHp\n" \
"1Wrjsok6Vjk4bwY8iGlbKk3Fp1S4bInMm/k8yuX9ifUSPJJ4ltbcdG6TRGHRjcdG\n" \
"snUOhugZitVtbNV4FpWi6cgKOOvyJBNPc1STE4U6G7weNLWLBYy5d4ux2x8gkasJ\n" \
"U26Qzns3dLlwR5EiUWMWea6xrkEmCMgZK9FGqkjWZCrXgzT/LCrBbBlDSgeF59N8\n" \
"9iFo7+ryUp9/k5DPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMBAf8E\n" \
"BTADAQH/MB0GA1UdDgQWBBRge2YaRQ2XyolQL30EzTSo//z9SzANBgkqhkiG9w0B\n" \
"AQUFAAOCAQEA1nPnfE920I2/7LqivjTFKDK1fPxsnCwrvQmeU79rXqoRSLblCKOz\n" \
"yj1hTdNGCbM+w6DjY1Ub8rrvrTnhQ7k4o+YviiY776BQVvnGCv04zcQLcFGUl5gE\n" \
"38NflNUVyRRBnMRddWQVDf9VMOyGj/8N7yy5Y0b2qvzfvGn9LhJIZJrglfCm7ymP\n" \
"AbEVtQwdpf5pLGkkeB6zpxxxYu7KyJesF12KwvhHhm4qxFYxldBniYUr+WymXUad\n" \
"DKqC5JlR3XC321Y9YeRq4VzW9v493kHMB65jUr9TU/Qr6cf9tveCX4XSQRjbgbME\n" \
"HMUfpIBvFSDJ3gyICh3WZlXi/EjJKSZp4A==\n" \
"-----END CERTIFICATE-----\n";

WiFiClientSecure client;

int WIFI_DELAY  = 100; //ms
DynamicJsonDocument doc(1024);

// oneM2M : CSE params

String CSE_M2M_ORIGIN = "3S2qIgRYgA:XyRZnyl7cp";

// oneM2M : resources' params
int TY_AE  = 2;
int TY_CNT = 3;
int TY_CI  = 4;
int TY_SUB = 23;

//// HTTP constants
int REQUEST_TIME_OUT = 5000; //ms


//MISC
int SERIAL_SPEED  = 115200;
String json_out="";

#define DEBUG

///////////////////////////////////////////


// Global variables
//WiFiServer server(LOCAL_PORT);    // HTTP Server (over WiFi). Binded to listen on LOCAL_PORT contant
//WiFiClient client;

// Method for creating an HTTP POST with preconfigured oneM2M headers
// param : url  --> the url path of the targted oneM2M resource on the remote CSE
// param : ty --> content-type being sent over this POST request (2 for ae, 3 for cnt, etc.)
// param : rep  --> the representaton of the resource in JSON format


String doGET(String url) {

  // Connect to the CSE address
client.setCACert(test_root_ca);

  Serial.println("\nStarting connection to server...");
  
  if (!client.connect(server, 443))
  {
    Serial.println("Connection failed!");
    return "error";
  }
  else {
    Serial.println("Connected to server!");
    String request = String() + "GET " + url + " HTTP/1.1\r\n" +
                      "Host: " + server + "\r\n" +
                      "X-M2M-Origin: " + CSE_M2M_ORIGIN + "\r\n" +
                      "Content-Type: application/json" + "\r\n" +
                      "Connection: close\r\n\n";
    // Make a HTTP request:
    client.println(request);

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        Serial.println("headers received");
        break;
      }
    }
    json_out = "";
    while (client.available()) {
       json_out = client.readString();
      Serial.println(json_out);
          json_out=json_out.substring(json_out.indexOf('{'),json_out.indexOf('}')+1);

      
    }

  client.stop();
  delay(5000);  //POST Data at every 20 seconds
  Serial.println();
  Serial.println("closing connection...");
  Serial.println(json_out);
  Serial.println("End of GET req");
  
  deserializeJson(doc, json_out);
  String vol=doc["m2m:cin"]["con"];
  Serial.println("in function vol: ");
  Serial.println(vol);
  return vol;
  }
    

}



String doPOST(String url, int ty, String rep) {
 client.setCACert(test_root_ca);

  Serial.println("\nStarting connection to server...");
  
  //POST Data
  
  const char* origin   = "3S2qIgRYgA:XyRZnyl7cp";
  if (!client.connect(server, 443))
    Serial.println("Connection failed!");
  else {
    Serial.println("Connected to server!");
    String request = String()+ "POST " + url + " HTTP/1.1\r\n" +
               "Host: " + server + "\r\n" +
               "X-M2M-Origin:" +  CSE_M2M_ORIGIN + "\r\n" +
               "Content-Type:application/json;ty="+ ty +"\r\n" +
               "Content-Length: "+ rep.length()+"\r\n" +
               "Connection: close\r\n\n" + 
               rep;
    // Make a HTTP request:
    client.println(request);

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        Serial.println("headers received");
        break;
      }
    }
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
    }

    client.stop();
  }
    delay(5000);
}

// Method for creating an ContentInstance(CI) resource on the remote CSE under a specific CNT (this is done by sending a POST request)
// param : ae --> the targted AE name (should be unique under the remote CSE)
// param : cnt  --> the targeted CNT name (should be unique under this AE)
// param : ciContent --> the CI content (not the name, we don't give a name for ContentInstances)
String createCI(String link, String ciContent) {
  String ciRepresentation =
    "{\"m2m:cin\": {"
    "\"con\":\"" + ciContent + "\""
    "}}";
  return doPOST(link, TY_CI, ciRepresentation);
}

void init_WiFi() {
  Serial.println("Connecting to  " + String(WIFI_SSID) + " ...");
  WiFi.persistent(false);
  WiFi.begin(WIFI_SSID, WIFI_PSWD);
  // wait until the device is connected to the wifi network
  while (WiFi.status() != WL_CONNECTED) {
    delay(WIFI_DELAY);
    Serial.print(".");
  }
  // Connected, show the obtained ip address
  Serial.println("WiFi Connected ==> IP Address = " + WiFi.localIP().toString());
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(SERIAL_SPEED);
  init_WiFi();// Connect to WiFi network
  

}

void loop() {
  // put your main code here, to run repeatedly:
  ////// Storing as a string in a single containers///////
    client.setCACert(test_root_ca);
    String arr = {doGET("https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-5/Node-1/Parameters/la")};
    Serial.println(arr);
//    String sped=doGET("https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-5/Node-1/Input-rpm/la");
//    Serial.println("Speed via get request");
//    Serial.println(sped);
//    String post_speed = "2255";
//    Serial.println("posting "+post_speed+"rpm");
//    createCI("https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-5/Node-1/Data/",post_speed);

  delay(5000);


}
