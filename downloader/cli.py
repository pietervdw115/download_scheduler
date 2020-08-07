import click
import os
import requests
import re
import schedule
import time

cwd = os.getcwd()
running = True


def get_filename_from_cd(cd):
    """
        Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def get_filename(url, r):
    """
        Find filename
    """
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    if filename is None:
        if url.find('/'):
            filename = url.rsplit('/', 1)[1]
            return filename
        else:
            click.secho("Something went wrong", fg='red')
    else:
        return filename


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(cwd + "/" + filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


@click.group()
def main():
    """
        Leeme se download scheduler
    """
    pass


@main.command()
def add():
    """
        Schedule a new download
    """
    url = click.prompt(
        "Please enter your download URL",
    )

    file = os.path.expanduser('~/.downloader/urls.txt')
    file_object = open(file, 'a')
    file_object.write(url + "\n")
    file_object.close()


@main.command()
def start():
    """
        Start the scheduler
    """
    global running
    running = True

    def job():
        click.secho("Downloads started", fg='green')
        urls = []
        file = os.path.expanduser('~/.downloader/urls.txt')
        url_file = open(file, 'r')
        count = 0

        while True:
            count += 1
            line = url_file.readline()
            if not line:
                break
            urls.append(line.strip())

        url_file.close()
        downloading = False
        for url in urls:
            downloading = True
            click.secho("Downloading from " + url, fg='cyan')
            url = url
            r = requests.get(url, allow_redirects=True, stream=True)
            filename = get_filename(url, r)
            if os.path.exists(filename):
                click.secho("Filename already exists \n Skipping...", fg='red')
            else:
                download_file(url, filename)
                click.secho(filename + " successfully downloaded.", fg='cyan', bold=True)
        if downloading:
            click.secho("All downloads completed", fg='green', bold=True)
        else:
            click.secho("Nothing to download", fg='red', bold=True)
            click.secho("Use `downloader add` to add downloads", fg='red', bold=True)
        global running
        running = False

    # schedule.every().day.at("00:00").do(job)
    schedule.every(10).seconds.do(job)

    while running:
        click.secho("Waiting for 00:00", fg='yellow')
        schedule.run_pending()
        # time.sleep(60)
        time.sleep(1)


@main.command()
def clear():
    """
        Clear download list
    """
    url_file = os.path.expanduser('~/.downloader/urls.txt')
    open(url_file, 'w').close()


@main.command()
def init():
    """
        Initialize the application
    """
    config_dir = os.path.expanduser('~/.downloader')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    url_file = os.path.expanduser(config_dir + '/urls.txt')
    with open(url_file, 'w') as urls:
        urls.write("")
    open(url_file, 'w').close()
