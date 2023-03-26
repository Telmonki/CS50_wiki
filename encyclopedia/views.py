from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown


from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):
    if util.get_entry(name) != None:
        content = markdown.markdown(util.get_entry(name))
        
        return render(request, "encyclopedia/title.html", {
            "title": content
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": "The page does not exist"
        }) 

def search_results(request):
    value = request.GET.get('q')

    if util.get_entry(value) != None:
        return render(request, "encyclopedia/title.html", {
            "title": util.get_entry(value)
        }) 
    else:
        query = request.GET.get('q')
        entries = [entry.lower() for entry in util.list_entries()]
        res = [i for i in entries if query in i]

        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": res
        })

def newpage(request):
    if request.method == "POST":
        form = util.NewTaskForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if title not in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(f"{title}")
            else:
                return render(request, "encyclopedia/title.html", {
                    "title": "The page already exists"
                }) 
    else:
        form = util.NewTaskForm()

    return render(request, "encyclopedia/newpage.html", {
        "form": form
    })

def editpage(request):
    latest_content = util.MarkdownContent.objects.last()
    if request.method == "POST":
        form = util.MarkdownContentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(content)
            return HttpResponseRedirect(f"{title}")

    else:
        form = util.MarkdownContentForm(instance=latest_content)

    return render(request, "encyclopedia/editpage.html", {
        "form": form
    })