# succo_google_quest

[![python](https://img.shields.io/badge/python-grey.svg)](https://www.python.org/)

This is **succo_google_quest**, a set of Python scripts to interact with the Google services through the [Google APIs](https://cloud.google.com/apis?hl=en). In particular,
- **succo_photos_quest** analyses the content of the user's [Google Photos](https://www.google.com/intl/en/photos/about/) book, providing information on all the albums and on all the photos/videos that aren't included in any album.
- **succo_mail_quest** allows to create as drafts or send multiple emails iteratively (e.g., to different recipients with custom subjects, bodies, attachments) through [Gmail](https://www.google.com/intl/en/gmail/about/).

This software is intended for those who already have an environment to develop with the Google APIs set up. Details on how to have this step done can be found [here](https://cloud.google.com/apis/docs/getting-started).

Basic dependencies:

[![google-auth-httplib2](https://img.shields.io/badge/google_auth_httplib2-grey.svg)](https://pypi.org/project/google-auth-httplib2/) [![google-auth-oauthlib](https://img.shields.io/badge/google_auth_oauthlib-grey.svg)](https://pypi.org/project/google-auth-oauthlib/) [![google-api-python-client](https://img.shields.io/badge/google_api_python_client-grey.svg)](https://github.com/googleapis/google-api-python-client) [![pandas](https://img.shields.io/badge/pandas-grey.svg)](https://pandas.pydata.org/) [![pip](https://img.shields.io/badge/pip-grey.svg)](https://pip.pypa.io/en/stable/)

All these are automatically installed if using [Anaconda](https://www.anaconda.com/) (this project was developed and tested with Anaconda 3) and generating the environment described in the environment.yml file.

Found a bug? Or simply have any questions, comments or suggestions you'd like to talk about? Feel free to contact me at <mattiasoldani93@gmail.com>. And brace yourself, for the best is yet to come!

---

### How it works

The succo_google_quest set can be downloaded either as a ZIP archive, from the Code drop-down menu [here](https://github.com/mattiasoldani/succo_google_quest), or directly from the terminal (open in your project working directory) via
```shell
git clone https://github.com/mattiasoldani/succo_google_quest.git
```
Note: the latter requires  [Git](https://git-scm.com/) installed on your machine.
