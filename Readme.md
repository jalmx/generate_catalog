# Generate a list or db from file html with the list of bought from aliexpress

Generate a list from the list bought in aliexpress, from html site (not selenium) throw a csv and json array]

---

Main file is `generate_list.py`, this generate a csv file with all items. Then automatic download all pictures from each link in the list.

Then have to exec `create_site.py` this file create a html with all the list.

Then for generate a `pdf`, have to exec the command with the html generated in the step before:

```commandline
wkhtmltopdf catalogo.html --enable-local-file-access [name_file].pdf  
```
