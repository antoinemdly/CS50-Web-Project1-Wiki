from django.shortcuts import render
from django.utils.safestring import mark_safe
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):

    markdown = util.get_entry(entry)
    safe_html = mark_safe(markdown2.markdown(markdown))
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": safe_html
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()

    # the query is a match
    if query in entries:
        return HttpResponseRedirect(reverse('entry', args=[query]))
    
    # the query is not a match
    list = []
    for entry in entries:
        print(entry)
        print(query)
        if query.lower() in entry.lower():
            list.append(entry)

    if list:
        return render(request, "encyclopedia/search.html", {
            "entries": list
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })
    
def new_page(request):
    if request.method == "POST":

        title = request.POST.get('title', '')
        markdown = request.POST.get('markdown', '')
        entries = util.list_entries()

        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/new_page.html", {
                    "title": title,
                    "markdown": markdown,
                    "error": 'This encyclopedia already exist'
                })
        
        with open(f"entries/{title}.md", 'a') as file:
            file.write(markdown)

        return render(request, "encyclopedia/new_page.html")
    
    return render(request, "encyclopedia/new_page.html")

def random(request):
    entries = util.list_entries()
    print(entries)
    entry = choice(entries)

    return HttpResponseRedirect(reverse('entry', args=[entry]))

def edit(request, entry):
    markdown = util.get_entry(entry)
    if request.method == 'POST':
        markdown = request.POST.get('markdown_final', '')

        with open(f"entries/{entry}.md", 'w') as file:
            file.write(markdown)
        
        return HttpResponseRedirect(reverse('entry', args=[entry]))

    return render(request, "encyclopedia/edit.html", {
        "markdown": markdown
    })
