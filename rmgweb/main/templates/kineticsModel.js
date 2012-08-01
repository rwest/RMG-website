var reftitle = '';
{% if entry.reference %}
reftitle += ' - {% filter split:','|first %}{{ entry.reference.authors.0 }}{% endfilter %}, {{ entry.reference.year }}';
reftitle = reftitle.replace('&#39;', "'");
{% endif %}

var kdata;
if (Plist.length > 0) {
    for (var j = 0; j < Plist.length; j++) {
        kdata = new Array();
        for (var i = 0; i < Tlist.length; i++) {
            kdata.push([1000./Tlist[i], Math.log(klist[j][i]) / Math.LN10]);
        }
        kseries.push(['{{ entry.result }}. {{ source }}{% if entry.index != -1 %}/{{ entry.index }}{% endif %} (' + Plist[j] + ' ' + Punits + '){% if not forward %} *{% endif %}' + reftitle, kdata]);
    }
}
else {
    kdata = new Array();
    for (var i = 0; i < Tlist.length; i++) {
        kdata.push([1000./Tlist[i], Math.log(klist[i]) / Math.LN10]);
    }
    kseries.push(['{{ entry.result }}. {{ source }}{% if entry.index != -1 %}/{{ entry.index }}{% endif %}' + reftitle + '{% if not forward %} *{% endif %}', kdata]);
}

var kseries2 = new Array();
if (Plist2.length > 0) {
    for (var i = 0; i < Tlist2.length; i++) {
        kdata = new Array();
        for (var j = 0; j < Plist2.length; j++) {
            kdata.push([Math.log(Plist2[j]) / Math.LN10, Math.log(klist2[j][i]) / Math.LN10]);
        }
        kseries2.push([Tlist2[i] + ' ' + Tunits, kdata]);
    }
}
