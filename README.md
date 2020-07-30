# License_Server
REST API that handles licensing for EFT_LAG switch

This is a REST api that I created for a lag switch that I made for a video game. The api has 1 endpoint /verify. The post reques to this endpoint contains 3 items
- Secret - A simple text string hardcoded into the client. This is just a simple measure to filter out non valid traffic
- Licence Key - The key that was given when the lag switch was purchased. This key is stored in a database along with how long it is valid for.
- HWID - The hardware ID of the computer that first activated the licence. This hardware id is computed using the Computer name, cpu id, and motherboard id.

All of this info is checked against the MariaDB. Depending on the outcome of this checked the correct JSON response is sent back to the client.

The client that uses this API is in a separate repo [here](https://github.com/jmcs811/EFT_LAG)
