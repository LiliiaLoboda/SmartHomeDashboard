function switchToggle(isChecked, toggle) {
    toggle.setAttribute('aria-checked', isChecked ? 'false' : 'true');
    toggle.classList.remove(isChecked ? 'mdc-switch--selected' : 'mdc-switch--unselected');
    toggle.classList.add(isChecked ? 'mdc-switch--unselected' : 'mdc-switch--selected');
}

function switchIcon(isChecked, id) {
    const icon = document.getElementById("icon_" + id)
    icon.style.fontVariationSettings = !isChecked ?
        "'FILL' 1, 'wght' 400, 'GRAD' 1, 'opsz' 48"
        : "'FILL' 0, 'wght' 400, 'GRAD' 1, 'opsz' 48";

    icon.style.color = !isChecked ? "orange" : "gray";
}

function updateToggle(toggle, id) {
    const isChecked = toggle.getAttribute('aria-checked') === 'true';
    switchToggle(isChecked, toggle);
    switchIcon(isChecked, id);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_device');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
            console.log('Toggle updated successfully.');
        } else {
            console.error('Toggle update failed.');
        }
    };
    const data = {value: toggle.getAttribute('aria-checked'), id}
    xhr.send(JSON.stringify(data));
}