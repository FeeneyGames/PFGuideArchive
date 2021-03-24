$.get("archive_links.html", function (links_html_str) {
    links_html = $.parseHTML(links_html_str);
    // iterate over class-label elements
    $(".class-label").each(function () {
        class_str = $(this).attr("id");
        empty_div = $.parseHTML("<div></div>");
        filled_div = $(empty_div).append($(links_html).filter("." + class_str));
        $("#" + class_str).after(filled_div);
        $("." + class_str).after("<br>");
    });
});
