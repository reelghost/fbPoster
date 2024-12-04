# FB Poster

## Overview

Welcome to the Facebook Video Poster script! This Python script automates the process of logging into Facebook and posting a video with an accompanying image. On the first run, it saves the login cookies to avoid the need for repeated logins in subsequent uses. This makes it efficient and seamless for regular use.

## Features

- **Automated Login**: Logs into Facebook using provided credentials.
- **Cookie Management**: Saves cookies on the first login and uses them for subsequent logins.
- **Media Posting**: Uploads media to your Facebook post.

## Requirements

- Python 3.10+
- `selenium`
- `webdriver-manager`
- `pickle`

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/reelghost/fbPoster.git
    cd fbPoster
    ```

2. **Install the Required Packages:**
    ```bash
    pip install selenium webdriver-manager
    ```

## Setup

1. **WebDriver Setup:**
    The script uses `webdriver-manager` to automatically manage the browser driver. Ensure you have the necessary browser installed (e.g., Chrome).

2. **Credentials:**
    Update the script with your Facebook credentials:
    ```python
    EMAIL = 'your-email@example.com'
    PASSWORD = 'your-password'
    ```

## Usage

Run the script using Python:
```bash
python facebook_video_poster.py
```

On the first run, the script will log you in using your credentials and save the cookies in a file. Subsequent runs will use these cookies to log in automatically.

## Troubleshooting

- **Login Issues**: If login fails, ensure your credentials are correct and try running the script again.
- **WebDriver Errors**: Make sure you have the latest version of the browser and `webdriver-manager` installed.

## Contributions

Feel free to contribute to this project by submitting issues or pull requests. Your feedback is appreciated!

## License

This project is licensed under the MIT License.


Enjoy posting on Facebook effortlessly! Other features to be posted soon.

