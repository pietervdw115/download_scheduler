import click
import os
import requests
import re
import schedule
import time

cwd = os.getcwd()


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
            print("Something went wrong")
    else:
        return filename


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


@click.group()
def main():
    """
        Leeme se download scheduler
    """
    pass


@main.command()
def download():
    """
        Schedule a new download
    """
    url = click.prompt(
        "Please enter your download URL",
    )

    file_object = open('urls.txt', 'a')
    file_object.write(url + "\n")
    file_object.close()


@main.command()
def start():
    """
        Start the scheduler
    """
    def job():
        urls = []
        url_file = open('urls.txt', 'r')
        count = 0

        while True:
            count += 1
            line = url_file.readline()
            if not line:
                break
            urls.append(line.strip())

        url_file.close()

        for url in urls:
            print(url)
            url = url
            r = requests.get(url, allow_redirects=True, stream=True)
            filename = get_filename(url, r)
            if os.path.exists(filename):
                click.secho("Filename already exists \n Skipping...", fg='red')
            else:
                download_file(url, filename)
                click.secho(filename + " successfully downloaded.", fg='green')
        click.secho("All downloads completed", fg='green')
        return schedule.CancelJob

    schedule.every().day.at("00:00").do(job)

    while True:
        schedule.run_pending()
        click.secho("Waiting for 00:00", fg='green')
        time.sleep(60)


@main.command()
def clear():
    """
        Clear download list
    """
    open('urls.txt', 'w').close()
