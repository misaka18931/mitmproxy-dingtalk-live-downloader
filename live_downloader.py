import logging
import uuid
import json
import requests as req
import os, shutil
import subprocess
from multiprocessing import Pool
from get_stream import download_bin

M3U8_REQUEST_PREFIX='[live-playback-room][/r/Adaptor/LiveStream/getLiveDetail success][response]'
STREAM_URL_PREFIX='https://dtliving-sh.dingtalk.com/live_hp/'
CACHE='tmp'
OUTPUT='output'
PARALLEL_CNT=1

def load(loader):
  CACHE='/tmp/dingtalk-downloader_' + str(uuid.uuid4())
  os.mkdir(CACHE);
  pass

def done():
  logging.info("dingtalk-downloader: cleaning caches.")
  shutil.rmtree(CACHE);
  

def request(flow): 
  if flow.request.pretty_host == "retcode.taobao.com" and "msg" in flow.request.query and flow.request.query["msg"][:75] == M3U8_REQUEST_PREFIX:
    res = json.loads(flow.request.query["msg"][75:])['liveInfo'];
    title = res['title'];
    liveUuid = res['liveUuid'];
    playUrl = res['playUrl'];
    savename = '{}[{}].mkv'.format(title, liveUuid);
    logging.info("found playUrl for stream '{}'[{}]: '{}'".format(title, liveUuid, playUrl));
    if not os.path.exists(os.path.join(OUTPUT, savename)):
      os.makedirs(os.path.join(CACHE, liveUuid));
      logging.info('downloading m3u8 playlist...');
      m3u = req.get(res['playUrl']).content.decode();
      logging.info('parsing m3u8 playlist...');
      slices = [];
      for line in m3u.splitlines():
        if line[0] != '#':
          slices.append((STREAM_URL_PREFIX+line, os.path.join(CACHE, line)));
#         r = req.get(STREAM_URL_PREFIX+line, stream=True);
#         with open(os.path.join(CACHE, line), 'wb') as dest:
#           for data in r.iter_content(chunk_size=1024):
#             dest.write(data);
      logging.info('downloading streams...');
      with Pool(processes=PARALLEL_CNT) as downloader:
        downloader.map(download_bin, slices)
      with open(os.path.join(CACHE, '{}.m3u8'.format(liveUuid)), 'w') as ply:
        ply.write(m3u);
      logging.info("starting ffmpeg...");
      subprocess.run(['ffmpeg', '-allowed_extensions', 'ALL', '-i', '{}.m3u8'.format(liveUuid), '-c', 'copy', os.path.abspath(os.path.join(OUTPUT, savename))], cwd=CACHE);
      logging.info("download completed.")

