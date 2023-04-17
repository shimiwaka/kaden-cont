# -*- coding: utf-8 -*-
from scapy.all import *
import time
import random
import sys

# 引数受け取る
args = sys.argv

# 初期設定
src = "192.168.0.2"
dst = "192.168.0.3"
sport = random.randint(10000,60000)
dport = 60001
ip = IP(dst = dst)

# コマンド読み込み
f = open("./cmd/" + args[1] + ".bin","rb")
cmd = f.read()
f.close()

# TCPパケット作成
tcp = TCP(sport = sport, dport = dport, flags = 'S', seq = 100, ack = 0)

# syn送信
syn = ip / tcp
# syn/ack受信
syn_ack = sr1(syn)

# ack送信
tcp.seq += 1
tcp.ack = syn_ack.seq + 1
tcp.flags = 'A'
ack = ip / tcp
send(ack)

# データ送信
payload = cmd
data = ip/tcp/payload
ack = sr1(data)

# 1秒待てばFINがくる
time.sleep(1)

# fin/ack送信
tcp.flags = 'FA'
tcp.seq = ack.ack
tcp.ack = ack.seq + 7
fin = ip / tcp

# ack受信
ack = sr1(fin)

# おわり