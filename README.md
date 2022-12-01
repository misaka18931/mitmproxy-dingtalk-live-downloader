# dingtalk live downloader

1. set up `mitmproxy`  
2. `mitmdump -s live_downloader.py`
3. click on streams in the dingtalk app to download.

Edit `PARALLEL_CNT` in `live_downloader.py` to download stream slices in parallel.
Default saving location is defined by the `OUTPUT` variable in `live_downloader.py`.