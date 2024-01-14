import sys

def progress_bar(iteration, total, title='progress', description='', length=20):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = "#" * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{title}: |{bar}| {percent}% {description}')
    sys.stdout.flush()