# Laravel Debugbar Enum

This project is a Python script that fetches data from a given URL, processes it, and stores it in a SQLite database. The script is designed to be run continuously, fetching new data at regular intervals and storing it in the database if it doesn't already exist.

## Features

- Fetches data from a specified URL
- Stores data in a SQLite database
- Excludes specified IP addresses from being stored
- Runs continuously, fetching new data at regular intervals

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/niranc/laravel-debugbar-enum.git
    cd laravel-debugbar-enum
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
```
python3 script.py --url "https://redacted.td/_debugbar/open?max=2000&offset=0" --timeout 30 --exclude-ips "x.x.x.x,y.y.y.y"
```

## Results

| IP Address   | URI                                                | Utime             |
|--------------|----------------------------------------------------|-------------------|
| xxx.xxx.xxx  | https://example.com/index.html                        | 1727149934.451536 |
| xxx.xxx.xxx  | https://example.com/api/v2/            | 1727149934.467426 |
| xxx.xxx.xxx  | https://example.com/secret_endpoint                        | 1727149934.480962 |
| xxx.xxx.xxx  | https://example.com/rest                           | 1727149930.913047 |
| xxx.xxx.xxx  | https://example.com/rest/favicon.ico               | 1727149930.933154 |
| xxx.xxx.xxx  | https://example.com/apidocs/swagger.json/favicon.ico| 1727149927.776736 |
| xxx.xxx.xxx  | https://example.com/apidocs/swagger.json           | 1727149927.836392 |

## Contributing

Pull requests are welcomed. If you have any suggestions or improvements, please feel free to create a pull request.

Thank you for your contributions!
