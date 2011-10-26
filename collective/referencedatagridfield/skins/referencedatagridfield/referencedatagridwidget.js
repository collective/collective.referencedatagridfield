function referencedatagrid_openBrowser(button, path, fieldName, at_url, fieldRealName, fieldTitleName, fieldLinkName, fieldUID)
{
	var timestamp=new Date().getTime();
	var button_class="selButton-" + timestamp;
	jq(button).toggleClass(button_class);
    atrefpopup = window.open(path + '/datagridreference_popup?sel_button=' + button_class + '&fieldName=' + fieldName + '&fieldRealName=' + fieldRealName +'&at_url=' + at_url + '&widget_title_id=' + fieldTitleName + '&widget_link_id=' + fieldLinkName + '&widget_id=' + fieldUID ,'referencebrowser_popup','toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=500,height=550');
}


function disablecurrentrelations(widget_id) {
    jq('ul#' + widget_id + ' :input').each(function (intIndex) {
        uid = jq(this).attr('value');
        cb = jq('input[rel=' + uid + ']');
        cb.attr('disabled', 'disabled');
        cb.attr('checked', 'checked');
    });
}

function refdatagridbrowser_setReference(widget_id, uid, label, multi, active_button, widget_title_id, link_title, widget_link_id, link_path) {
	var element = null, label_element = null, current_values = null, i = null, list = null, li = null, input = null, up_element = null, down_element = null, container = null;
    var active_tr = jq('input.'+active_button).parents('tr[id=datagridwidget-row]');
	if (typeof(active_tr) != "undefined" && typeof(link_title) != "undefined" && typeof(link_path) != "undefined" && typeof(widget_title_id) != "undefined" && typeof(widget_link_id) != "undefined") {
        jq('#' + widget_id, active_tr).attr("value", uid);
        title = jq('#' + widget_title_id, active_tr);
        title.attr("value", link_title);
        title.addClass("not-changed-title-field");
        title.attr("default_value", link_title);
        title.blur(triggerTitleClass);
        title.focus(triggerOnFocusStyles);
        link = jq('#' + widget_link_id, active_tr);
        link.attr('readonly', false);
        link.attr('value', link_path);
        link.attr('readonly', true);
        link.addClass("hidden-field");
    }
    else 
        if (multi === 0) {
            jq('#' + widget_id).attr('value', uid);
            jq('#' + widget_id + '_label').attr('value', label);
        }
        else {
            current_values = jq('#' + widget_id + ' input');
            for (i = 0; i < current_values.length; i++) {
                if (current_values[i].value === uid) {
                    return false;
                }
            }
            list = document.getElementById(widget_id);
            if (list === null) {
                container = jq('#archetypes-fieldname-' + widget_id + ' input + div');
                if (!container.length) {
                    container = jq('#archetypes-fieldname-value input + div');
                }
                container.after('<ul class="visualNoMarker" id="' + widget_id + '"></ul>');
                list = document.getElementById(widget_id);
            }
            li = document.createElement('li');
            label_element = document.createElement('label');
            input = document.createElement('input');
            input.type = 'checkbox';
            input.value = uid;
            input.checked = true;
            input.name = widget_id + ':list';
            label_element.appendChild(input);
            label_element.appendChild(document.createTextNode(' ' + label));
            li.appendChild(label_element);
            li.id = 'ref-' + widget_id + '-' + current_values.length;
            sortable = jq('input[name=' + widget_id + '-sortable]').attr('value');
            if (sortable === '1') {
                up_element = document.createElement('a');
                up_element.title = 'Move Up';
                up_element.innerHTML = '▲';
                up_element.onclick = function () {
                    refdatagridbrowser_moveReferenceUp(this);
                    return false;
                };
                li.appendChild(up_element);
                down_element = document.createElement('a');
                down_element.title = 'Move Down';
                down_element.innerHTML = '▼';
                down_element.onclick = function () {
                    refdatagridbrowser_moveReferenceDown(this);
                    return false;
                };
                li.appendChild(down_element);
            }
            list.appendChild(li);
            console.log(list);
            console.log(li);
            input.checked = true;
        }
}

function refdatagridbrowser_removeReference(widget_id, multi) {
    var x = null, element = null, label_element = null, list = null;
    if (multi) {
        list = document.getElementById(widget_id);
        for (x = list.length - 1; x >= 0; x--) {
            if (list[x].selected) {
                list[x] = null;
            }
        }
        for (x = 0; x < list.length; x++) {
            list[x].selected = 'selected';
        }
    }
    else {
        jq('#' + widget_id).attr('value', "");
        jq('#' + widget_id + '_label').attr('value', "");
    }
}

function refdatagridbrowser_moveReferenceUp(self) {
    var elem = self.parentNode, eid = null, pos = null, widget_id = null, newelem = null, prevelem = null, arrows = null, cbs = null;
    if (elem === null) {
        return false;
    }
    eid = elem.id.split('-');
    pos = eid.pop();
    if (pos === 0) {
        return false;
    }
    widget_id = eid.pop();
    newelem = elem.cloneNode(true);
    cbs = newelem.getElementsByTagName("input");
    if (cbs.length > 0) {
        cbs[0].checked = elem.getElementsByTagName("input")[0].checked;
    }
    prevelem = document.getElementById('ref-' + widget_id + '-' + (pos - 1));
    arrows = newelem.getElementsByTagName("a");
    arrows[0].onclick = function () {
        refdatagridbrowser_moveReferenceUp(this);
    };
    arrows[1].onclick = function () {
        refdatagridbrowser_moveReferenceDown(this);
    };
    elem.parentNode.insertBefore(newelem, prevelem);
    elem.parentNode.removeChild(elem);
    newelem.id = 'ref-' + widget_id + '-' + (pos - 1);
    prevelem.id = 'ref-' + widget_id + '-' + pos;
}

function refdatagridbrowser_moveReferenceDown(self) {
    var elem = self.parentNode, eid = null, pos = null, widget_id = null, current_values = null, newelem = null, nextelem = null, cbs = null, arrows = null;
    if (elem === null) {
        return false;
    }
    eid = elem.id.split('-');
    pos = parseInt(eid.pop(), 10);
    widget_id = eid.pop();
    current_values = jq('#' + widget_id + ' input');
    if ((pos + 1) === current_values.length) {
        return false;
    }
    newelem = elem.cloneNode(true);
    cbs = newelem.getElementsByTagName("input");
    if (cbs.length > 0) {
        cbs[0].checked = elem.getElementsByTagName("input")[0].checked;
    }
    arrows = newelem.getElementsByTagName("a");
    arrows[0].onclick = function () {
        refdatagridbrowser_moveReferenceUp(this);
    };
    arrows[1].onclick = function () {
        refdatagridbrowser_moveReferenceDown(this);
    };
    nextelem = document.getElementById('ref-' + widget_id + '-' + (pos + 1));
    elem.parentNode.insertBefore(newelem, nextelem.nextSibling);
    elem.parentNode.removeChild(elem);
    newelem.id = 'ref-' + widget_id + '-' + (pos + 1);
    nextelem.id = 'ref-' + widget_id + '-' + pos;
}

function showMessageRDG(message) {
    jq('#messageTitle').text(message);
    jq('#message').show();
}

function submitHistoryForm() {
    var form = document.history;
    var path = form.path.options[form.path.selectedIndex].value;
    form.action = path;
    form.submit();
}

function pushToHistory(url) {
    var history = jq(document).data('atrb_history');
    history.push(url);
    jq(document).data('atrb_history', history);
}

function resetHistory() {
    jq(document).data('atrb_history', []);
}

function popFromHistory() {
    var history = jq(document).data('atrb_history');
    value = history.pop();
    jq(document).data('atrb_history', history);
    return value;
}

dataGridFieldFunctions.addReferenceDataGridRow = function (id) {
    this.addRow(id);
    var active_row = jq("#datagridwidget-tbody-" + id + " tr#datagridwidget-row:last");
    jq(active_row).prepRefPopup();
}
dataGridFieldFunctions.addReferenceDataGridRowAfter = function (currnode) {
    this.addRowAfter(currnode);
    var tbody = jq(currnode).parents("[id^=datagridwidget-tbody-]");
    var rows = jq("#datagridwidget-row", tbody);
    var curr_row = jq(currnode).parents("tr#datagridwidget-row");
    var active_row = rows[rows.index(curr_row) - 1];
    jq(active_row).prepRefPopup();
}
dataGridFieldFunctions.OriginalUpdateOrderIndex = dataGridFieldFunctions.updateOrderIndex;
dataGridFieldFunctions.updateOrderIndex = function (tbody) {
    var rows, tr, idx, ov, ov_id, under_idx, new_ov_id
    this.OriginalUpdateOrderIndex(tbody);
    rows = jq("#datagridwidget-row", tbody);
    for (var i = 0; i < rows.length; ++i) {
        tr = rows[i];
        order_tag = jq("input[id^=orderindex__]", tr);
        idx = order_tag.attr("value");
        ov = jq("input.addreferencedatagrid", tr);
        ov_id = ov.attr("rel");
        under_idx = ov_id.lastIndexOf("_");
        base_id = (under_idx >= 0) ? ov_id.substring(0, under_idx) : "#atrb";
        new_ov_id = base_id + "_" + idx;
        ov.attr("rel", new_ov_id);
        jq("div[id^=atrb_]", tr).attr("id", new_ov_id.substring(1));
    }
}
function triggerTitleClass(e) {
    var element = jq(e.target);
    var current = element.attr("value");
    var initial = element.attr("default_value");
    if (initial == null || current == null) 
        return;
    if (initial == current) {
        element.attr("class", "not-changed-title-field");
    }
    else {
        element.attr("class", "changed-title-field")
    }
}

function triggerOnFocusStyles(e) {
    jq(e.target).attr("class", "changed-title-field")
}
