var default_suggestion = document.id("id_amount").get('value');
document.id("id_suggestions").get('value').split(/-/).each(function(e) {
    if (e != "") {
        var element = new Element('p', {text: e.replace(/\.00$/, ""), 'class': 'alt'});
        if (e == default_suggestion) { element.addClass("active"); }
        document.id("donation-alternatives").grab(element);
    }
});
