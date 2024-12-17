REDDIT_HEADERS = {
    'accept': 'text/vnd.reddit.partial+html, text/html;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'rdt=27e463ccfe7ce1ed06eb67564b03dba9; edgebucket=LWkXtObvVTGygR7muE; csv=2; g_state={"i_l":0}; loid=0000000000000lpanb.2.1425047371373.Z0FBQUFBQm1zU1ZwVTliRHVFcHNjY2tDZ1pBc1V5bnNYVXBvOGlpQ0JZRTFLaThqR3NBYlFNaG51RGRXdUxmLUh4REdHaWdEYjBtSkxlTWF5UFFOVnJ5OGcyZVVUQjdhaF94STUwNVozOWxxdG00UE5EeXZ6ckNwZHdRbjVHanhSQ2N5OFJYRi1SR2U; theme=2; __stripe_mid=1a5a8411-d554-41e3-aca2-3009b363c50c76f31e; reddit_chat_path=/room/\\u0021c5fuYVnUUndrxRUawoxGSIjiokLC83KLO0iIsfRHPk4%[253Areddit.com](http://253areddit.com/); reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9scGFuYiIsImV4cCI6MTc0OTU3NzgxOS44NDQzNzIsImlhdCI6MTczMzkzOTQxOS44NDQzNzIsImp0aSI6IlA5RS16RDNjd3dTd19Vb2d3R2o4dmpPcGtwTWxidyIsImNpZCI6ImNvb2tpZSIsImxjYSI6MTQyNTA0NzM3MTM3Mywic2NwIjoiZUp5S2pnVUVBQURfX3dFVkFMayIsInYxIjoiMzY0NTIxMzUlMkMyMDI0LTA4LTA1VDE5JTNBMTclM0E1OCUyQzE1Y2M5NzU0NGJhZTdjNmZkZDBkMDAzM2NjMjJmNzc4MTk5NmJiMzciLCJmbG8iOjF9.OtNzxTsikTYWLTlwHggBpAUWOJcm73g72uzj7iPrJGXnyFyyTby193GYsdFeny_TxNlI7c3p6PXWOaOc4cJDHHJCVD3bjgoClpynLJ8oXAl6YzoKd0MqzBgUagL_hCZsdsoejuHDtrzDqZlor9yU2LZVt_b0743m2tBbHU5QFct9JnyJfoa9ujCw8MUXgM1XfXmu8HuAnDMOu4N9Jvi7TEB9ix6gKOh8X3yjaxF5-TPmVTW0iXXO-BFeT9CnKZ6Vy3ufaBqEVyFUXL0uOSESkFhsyVGhQ8rvgLSE58UCvHic7OHYOMObNLBUzkqyzhkeutE77kgOiWa-8GapJP5EaQ; pc=7a; reddit_chat_view=closed; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzM0NDE5ODMyLjQ5MjIwOCwiaWF0IjoxNzM0MzMzNDMyLjQ5MjIwOCwianRpIjoiMnBXcHZzNlgwUUJnUmxFSnZaWGtJNVlNQlk5YXJRIiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml9scGFuYiIsImFpZCI6InQyX2xwYW5iIiwibGNhIjoxNDI1MDQ3MzcxMzczLCJzY3AiOiJlSnhra2RHT3REQUloZC1GYTVfZ2Y1VV9tMDF0Y1lhc0xRYW9rM243RFZvY2s3MDdjRDRwSFA5REtvcUZEQ1pYZ3FuQUJGZ1RyVERCUnVUOW5MbTNnMmlOZTh0WXNabkNCRm13RkRya21MR3NpUVFtZUpJYXl4c21vSUxOeUZ5dXRHTk5MVDBRSnFoY01yZUZIcGMyb2JrYmk1NmRHRlc1ckR5b3NWZmwwdGpHRkxZbnhqY2JxdzJwdUM2bk1rbkxRdmtzWHZUak45VzM5dm16X1NhMEo4T0txdW1CM2hsSkNHNHNmcGltM2Q5VGs1NnRDeGExOTNxUTJ1ZDYzSzU5MWl3ME83ZWY2X2xySXhtWFkyaC1KdnQzMXktaEE0ODhMelBxQUVhczRVY1pkbVFkX2xVSFVMbWdKR01KNHRNSTVNcmwyMzhKdG12VHY4YnRFejk4TS1LbU5feldETlJ6Q2VMUXBfSDFHd0FBX184UTFlVFIiLCJyY2lkIjoiamVLZEtTbzVqdVYxaUdKTGNiMFBaTnB2WWttaDVxMWpzYzJRUGFRUi15RSIsImZsbyI6Mn0.kwmkjm3_qcorN774FDfhQu9JhxlkgQBQK5IBGYGJa7QPADgk5YjfJOLea711YKu1-ou-irX0xaVwxB8gzU4ulC15mll0c5R4rchrP29NW-APKfB-rAyCwrrOzGYKmqpRgQviz-dFOCqrfT5inATHJ16VRRQEaLa5DojGXcsRYHT-s5Z-KO1FZXrR11DM19BlTbgKevTY7ua-6ypBDNYyYNvxyyUF88VXvfu9p4r2l8XXSSgY4dF8Sc2sw9I0NFHgpvyQiX2zRA00fVlgIB5yu0Aek0ebZJNPaT47KjTam9EhzGvFCuqNKe6Bfaoj72eX5HtfHxSWeitZSXuhK9zRow; t2_lpanb_recentclicks3=t3_17q4hjc%2Ct3_1hfrzk9%2Ct3_1hft0lt%2Ct3_1hfku8u%2Ct3_18z5ivk%2Ct3_1hfmul8%2Ct3_1hf80pc%2Ct3_1hcrpln%2Ct3_15zoq1f%2Ct3_1hctwq8; session_tracker=rngmriaglpjfnerbon.0.1734394506693.Z0FBQUFBQm5ZTUtLM1lpai11SjdhOU9oSFVVUkRoSzNMUXp5c3FKd1IwdzNoRFJpLXAtRWtxVnRvYmI4TWVHSkFMUlp2a2Vva2dQN1A5azhxbTVRbms4UF9zY3JReVUzRlNrYkg3ejJPRnBLUDVEdXZ2bkR0VFlVbW5JSWk3NjR2RkRndWlCemNMbGk; csrf_token=3141e5a9e25e5d193495f60e553292d2',
    'dnt': '1',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.reddit.com/r/ChronicPain/',
    'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
