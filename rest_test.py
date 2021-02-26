import keys
import rest_client as r

ftx = r.FtxClient(keys.API_KEY, keys.API_SECRET)

print(ftx.get_usd_value())