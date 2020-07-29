#!/usr/bin/python
# -*- coding: utf-8 -*-

#this is display the strength of ligh 0.2sec each

# Bezelie Sample Code for Raspberry Pi : アナログ入力のサンプル
# ラズパイにADコンバータとアナログセンサーを接続しておいてください。

# ライブラリの読み込み
import RPi.GPIO as GPIO
import datetime
from time import sleep

# MCP3204からSPI通信で12ビットのデジタル値を取得。4チャンネル使用可
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

# 初期設定
GPIO.setmode(GPIO.BCM)

# 変数
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

# 関数
def main():
    try:
        print("開始します")
        inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print("Last valid input: " + str(datetime.datetime.now()))
        print(inputVal0)
        f1 = open("/home/pi/ex7/light.txt", "a")
        f2 = open("/home/pi/ex7/data.txt", "a")
        f1.write("\n\nLast valid input: " + str(datetime.datetime.now()))
        f2.write("\n\nLast valid input: " + str(datetime.datetime.now()))
        f1.write("\nLight: " + str(inputVal0))
        f2.write("\nLight: " + str(inputVal0))
        f1.close()
        f2.close()
        #sleep(10)

    except KeyboardInterrupt:
        print("終了しました")
        GPIO.cleanup()                     # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
            
