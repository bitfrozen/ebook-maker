import zipfile, os, argparse
import subprocess

def create_archive(path='/path/to/our/epub/directory'):
    ''' Create the ZIP archive. The mimetype must be the first file and must not be compressed.'''
    epub_name = '%s.epub' % os.path.basename(path)

    os.chdir(path)

    # Open a new zipfile for writing
    epub = zipfile.ZipFile(epub_name, 'w')

    # Add the mimetype file first and set it to be uncompressed
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)

    # Add directories and 1 dir deep files to zip file
    for d in os.listdir('.'):
        p_path = os.path.join(path, d)
        if os.path.isdir(p_path) and (d != '.vscode'):
            for root, dirs, files in os.walk(d):
                for filename in files:
                    print("Adding item {} to epub".format(filename))
                    epub.write(os.path.join(root,filename), compress_type=zipfile.ZIP_DEFLATED)

    epub.close()

def create_mimetype(path='/path/to/our/epub/directory'):
    f = os.path.join(path, 'mimetype')
    f = open(f, 'w')
    f.write('application/epub+zip')
    f.close()

def run_kindlegen(path_to_kindlegen='/path/to/kindlegen/file', path_to_epub='/path/to/epub/file'):
    result = subprocess.run([path_to_kindlegen, path_to_epub], stdout=subprocess.PIPE)
    print (result.stdout.decode('utf-8'))


# Get working directory
parser = argparse.ArgumentParser("epub_maker")
parser.add_argument("path", help="Path to directory containing epub files", type=str)
parser.add_argument("kindlegen", help="Path to kindlegen file", type=str)
args = parser.parse_args()
working_directory = args.path
kindlegen_path = args.kindlegen

os.chdir(working_directory)

# Remove previously generated files
epub_name = '%s.epub' % os.path.basename(working_directory)
mobi_name = '%s.mobi' % os.path.basename(working_directory)
if os.path.exists(epub_name):
    os.remove(epub_name)
if os.path.exists(mobi_name):
    os.remove(mobi_name)

# Create mimetype file if it doesn't exist
if not os.path.exists('mimetype'):
    create_mimetype(working_directory)

# Create epub file
create_archive(working_directory)

# Create mobi file
run_kindlegen(kindlegen_path, os.path.join(working_directory, epub_name))