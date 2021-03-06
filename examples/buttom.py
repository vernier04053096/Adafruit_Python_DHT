@@ -20,8 +20,28 @@
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 import sys
-
 import Adafruit_DHT
+import time
+import httplib, urllib
+import json
+deviceId = "Dt3t808n"
+deviceKey = "768S0iu7dtCJDZYw"
+def post_to_mcs(payload): 
+	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
+	not_connected = 1 
+	while (not_connected):
+		try:
+			conn = httplib.HTTPConnection("api.mediatek.com:80")
+			conn.connect() 
+			not_connected = 0 
+		except (httplib.HTTPException, socket.error) as ex: 
+			print "Error: %s" 
+			 # sleep 10 seconds 
+	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
+	response = conn.getresponse() 
+	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
+	data = response.read() 
+	conn.close() 
 
 
 # Parse command line parameters.
 @@ -47,8 +67,16 @@
 # the results will be null (because Linux can't
 # guarantee the timing of calls to read the sensor).
 # If this happens try again!
-if humidity is not None and temperature is not None:
-    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
-else:
-    print('Failed to get reading. Try again!')
-    sys.exit(1)
+while True:
+	h0, t0= Adafruit_DHT.read_retry(sensor, pin)
+	humidity, temperature = Adafruit_DHT.read_retry(11,4)
+	if humidity is not None and temperature is not None:
+		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
+		payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},
+			{"dataChnId":"Temperature","values":{"value":t0}}]} 
+		post_to_mcs(payload)
+		time.sleep(10) 
+	else:
+		print('Failed to get reading. Try again!')
+		sys.exit(1)
+
