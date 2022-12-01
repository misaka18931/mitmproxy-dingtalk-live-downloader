import requests as req

def download_bin(u: tuple):
  url, dest = u
  try:
    r = req.get(url, stream=True);
    with open(dest, 'wb') as f:
      for data in r.iter_content(chunk_size=4096):
        f.write(data);
  except Exception as e:
    logging.error("error downloading file:", e);
