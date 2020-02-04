"""
Author: Rob Raddi
Date: 01/16/20

Description of program:
    This program will generate a markdown file named 'Home.md' that will be
act as the Voelz Lab wiki table of contents.
"""

import glob,os,sys

class Categories(object):

    def __init__(self, files, verbose=False):
        self.files = files
        self.verbose = verbose
        self.categories = list()
        self.pages = list()
        self.dict = {"page": self.pages,
                "category": self.categories}

    def get_categories(self):
        """Pull a categories and/or subcategories from a wiki files."""

        for file in self.files:
            f = open(file, "r")
            f.seek(0)
            self.dict['page'].append(file.split("/")[-1])
            # look at the first 5 lines to see if there's a category
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
                self.dict['category'].append("Miscellaneous")
            f.close()


def write_markdown(file, headers, pages):
    """Write the new Home.md file."""

    categories_ = list(dict.fromkeys(headers))
    # Make sure that the 'None' Category is last in the list
    if "Miscellaneous" in categories_:
        categories_.remove("Miscellaneous")
        categories_.append("Miscellaneous")
    contents = str()
    # 0. Add link to help page for wiki
    contents+='''<h4><a href="Wiki-Help">Wiki Help</a></h4>\n\n'''

    # 1. Create Table of Contents
    contents+='''<table align="center" \
            style="width:100%;margin-left:auto;margin-right:auto">\
            <tr><th>Table of Contents</th></tr>\n'''
    for i in range(len(categories_)):
        contents_header='''<tr><td><a href="#%s">%s</a></td></tr>\n'''%(
                categories_[i].replace(" ","-").lower(), categories_[i].capitalize())
        contents += contents_header

    # End table and carriage return a few times
    contents += """\n</table>\n\n\n"""

    # 2. Create lists of files under table of contents
    for i in range(len(categories_)):
        contents += """<h1>%s</h1>\n<ul class="bordered">\n"""%(str(categories_[i].capitalize()))
        pages_ = [pages[k] for k in range(len(pages)) if str(headers[k]) == str(categories_[i])]
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
    C = Categories(files, testing)
    C.get_categories()
    print("\n")
    print("Writing %s ..."%(homepage))
    write_markdown(file=homepage, headers=C.dict['category'], pages=C.dict['page'])
    print("Done!")


