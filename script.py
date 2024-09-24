import requests
import argparse
import time
import sqlite3
from R2Log import logger
from rich.console import Console

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to fetch JSON data from a URL and store IP, URI, and utime in SQLite.')
    parser.add_argument('--url', type=str, required=True, help='URL to fetch JSON data from')
    parser.add_argument('--timeout', type=int, default=30, help='Interval in seconds between requests')
    parser.add_argument('--exclude-ips', type=str, default="", help='Comma-separated list of IPs to exclude, e.g., "1.1.1.1,2.2.2.2"')
    return parser.parse_args()

def connect_to_sqlite():
    try:
        conn = sqlite3.connect('debugbar.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                ip TEXT NOT NULL,
                uri TEXT NOT NULL,
                utime INTEGER NOT NULL
            )
        ''')
        conn.commit()
        return conn, cursor
    except sqlite3.Error as e:
        logger.error(f"Error connecting to SQLite: {e}")
        exit(1)

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

def store_data(cursor, conn, data, url, exclude_ips):
    exclude_ips_list = exclude_ips.split(",")
    for item in data:
        ip = item.get('ip')
        uri = item.get('uri')
        utime = item.get('utime')
        if ip and uri and utime and ip not in exclude_ips_list:
            uri = f"{url}{uri}"
            cursor.execute('SELECT * FROM requests WHERE ip=? AND uri=? AND utime=?', (ip, uri, utime))
            if not cursor.fetchone():
                try:
                    cursor.execute('INSERT INTO requests (ip, uri, utime) VALUES (?, ?, ?)', (ip, uri, utime))
                    conn.commit()
                    logger.info(f"IP: {ip}, URI: {uri}, Utime: {utime}")
                except sqlite3.OperationalError as e:
                    logger.error(f"SQLite OperationalError: {e}")
            else:
                logger.verbose(f"Already exists: {{'ip': ip, 'uri': uri, 'utime': utime}}")

def main():
    args = parse_arguments()
    conn, cursor = connect_to_sqlite()

    while True:
        data = fetch_data(args.url)
        url = '/'.join(args.url.split('/')[:3])
        if data:
            store_data(cursor, conn, data, url, args.exclude_ips)
        with console.status("[bold green]Waiting between requests...[/bold green]"):
            time.sleep(args.timeout)

if __name__ == '__main__':
    main()