"""
Author: Rob Raddi
Date: 01/16/20

Description of program:
    This program will generate a markdown file (Home.md) for a GitHub wiki.
"""

import glob,os,sys

class Tags(object):

    def __init__(self, files, verbose=False):
        self.files = files
        self.verbose = verbose
        self.tags = list()
        self.pages = list()
        self.dict = {"page": self.pages,
                "tag": self.tags}

    def get_tags(self):
        """Pull a tags and/or subtags from a wiki files."""

        for file in self.files:
            f = open(file, "r")
            f.seek(0)
            self.dict['page'].append(file.split("/")[-1])
            # look at the first 5 lines to see if there's a tag
            lines = f.readlines(5)
            if "<!--" in str(lines).strip():
                for line in lines:
                    key = line.split(":")[0].strip().lower()
                    value = line.split(":")[-1].strip().lower()
                    if value == "None":
                        pass
                    if key in self.dict.keys():
                        self.dict[key].append(value)
            else:
                self.dict['tag'].append("Miscellaneous")
            f.close()


def write_HTML(file, headers, pages):
    """Write the new Home.md file."""

    tags_ = list(dict.fromkeys(headers))
    # Make sure that the 'None' tag is last in the list
    if "Miscellaneous" in tags_:
        tags_.remove("Miscellaneous")
        tags_.append("Miscellaneous")
    contents = str()
    # 0. Add link to help page for wiki
    contents+='''<h4><a href="Wiki-Help">Wiki Help</a></h4>\n\n'''

    # 1. Create Table of Contents
    contents+='''<table align="center" \
            style="width:100%;margin-left:auto;margin-right:auto">\
            <tr><th>Table of Contents</th></tr>\n'''
    for i in range(len(tags_)):
        contents_header='''<tr><td><a href="#%s">%s</a></td></tr>\n'''%(
                tags_[i].replace(" ","-").lower(), tags_[i].capitalize())
        contents += contents_header

    # End table and carriage return a few times
    contents += """\n</table>\n\n\n"""

    # 2. Create lists of files under table of contents
    for i in range(len(tags_)):
        contents += """<h1>%s</h1>\n<ul class="bordered">\n"""%(str(tags_[i].capitalize()))
        pages_ = [pages[k] for k in range(len(pages)) if str(headers[k]) == str(tags_[i])]
        for page in pages_:
            contents += """<li style="list-style-type:none">\
                    <a target='_blank' href='%s'>%s</a></li>\n"""%(
                    page.split(".")[0], page.split(".")[0].replace("-"," "))
        contents += """</ul>\n\n\n"""

    with open(file, "w") as f:
        f.write(contents)
        f.close()



if __name__ == "__main__":

    testing = False #True
    homepage = "Home.md" # wiki homepage
    print("Organizing...\n")
    # grab all the markdown and mediawiki files
    wiki = "./*.wiki/"
    extensions = ["*.md", "*.mediawiki", "*.asciidoc", "*.org",
            "*.pod", "*.rdoc", "*.rest", "*.textile"]
    files = list()
    for ext in extensions:
        files += glob.glob(wiki+"%s"%(ext))
    ignore = [homepage, homepage.split(".")[0]+".mediawiki",
            "_Sidebar.md", "_Footer.md", "Wiki-Help.md"]
    for file in ignore:
        try:
           files.remove(wiki+"%s"%(file))
        except: ValueError
    C = Tags(files, testing)
    C.get_tags()
    print("\n")
    print("Writing %s ..."%(homepage))
    write_HTML(file=homepage, headers=C.dict['tag'], pages=C.dict['page'])
    print("Done!")


