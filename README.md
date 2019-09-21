## Google Chrome and ChromeDriver are needed

Download the [Google Chrome][Chrome].

Download the [ChromeDriver][ChromeDriver] that match the Google Chrome version. (Windows download `chromedriver_win32.zip`)

Move the `chromedriver.exe` to `tool` folder


## Usage

Make sure that you have installed the `Google Chrome` and put the `ChromeDriver` to the `tool` driver

Modify this line in `baha_friends_follows_handler.py`: `BAHA = BahaFriends('----0')`

From left to right correspond to `叭哈創推實`.

`-` means keep the same state.

`0` means change to unsubscribe.

`1` means change to subscribe.

e.g., `----0` means unsubscribe `實` from all IDs that not be excluded, and `叭哈創推` keeps the same.

Write the IDs you want to exclude to the `exclude_ids.txt` line by line.

Run `baha_friends_follows_handler.py`

You need to manually login your account.

After logging in, you should wait for redirecting on the [homepage][Bahamut].

The program will auto run, you leave it alone.

You can check the `log.log` file when it finished.

[Chrome]: https://www.google.com/intl/zh-TW/chrome/

[ChromeDriver]: https://sites.google.com/a/chromium.org/chromedriver/

[Bahamut]: https://www.gamer.com.tw/