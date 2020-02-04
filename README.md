## `Wiki-Organizer`
####  is a very basic GitHub Action that automatically generates a Home.md for a GitHub wiki.

Globs all possible file extensions used in a GitHub wiki: 
`["*.md", "*.mediawiki", "*.asciidoc", "*.org","*.pod",
"*.rdoc", "*.rest", "*.textile"]`

### Notes for creating a new page in the wiki:

#### Example: Adding category

Add a category label inside an html comment (hidden when rendering).

```HTML
<!--
Category: Projects
-->
```

### What if no tag?

The file will automatically be placed under the `Miscellaneous` section in the table of contents.

##### Publishing GitHub Actions


[Publishing packages to GitHub Packages](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/publishing-nodejs-packages#publishing-packages-to-github-packages)

[Creating and using encrypted secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets)





