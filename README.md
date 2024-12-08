# FB Poster

## Overview

Welcome to the Facebook Video Poster script! This Python script automates the process of logging into Facebook and posting a post with an accompanying image. On the first run, it saves the login cookies to avoid the need for repeated logins in subsequent uses. This makes it efficient and seamless for regular use.

## Features

- **Automated Login**: Logs into Facebook using provided credentials.
- **Media Posting**: Uploads media to your Facebook post.

## Requirements

- Python 3.10+
- `selenium`

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/reelghost/fbPoster.git
    cd fbPoster
    ```

2. **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. **WebDriver Setup:**
    The script uses `webdriver-manager` to automatically manage the browser driver. Ensure you have the necessary browser installed (e.g., Chrome).


## Usage

Run the script using Python:
```bash
python main.py
```

On the first run, the script will log you in using your credentials and save them. Subsequent runs will use these credentials.

## Troubleshooting

- **Login Issues**: If login fails, ensure your credentials are correct and try running the script again.

## Contributions

Feel free to contribute to this project by submitting issues or pull requests. Your feedback is appreciated!

## License

This project is licensed under the MIT License.


Enjoy posting on Facebook effortlessly! Other features to be posted soon.

