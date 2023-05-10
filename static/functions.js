function switchToggle(toggle, isChecked) {
    toggle.setAttribute('aria-checked', isChecked ? 'false' : 'true');
    toggle.classList.remove(isChecked ? 'mdc-switch--selected' : 'mdc-switch--unselected');
    toggle.classList.add(isChecked ? 'mdc-switch--unselected' : 'mdc-switch--selected');
}

function switchIcon(id, color, isChecked) {
    const icon = document.getElementById("icon_" + id)
    icon.style.fontVariationSettings = !isChecked ?
        "'FILL' 1, 'wght' 400, 'GRAD' 1, 'opsz' 48"
        : "'FILL' 0, 'wght' 400, 'GRAD' 1, 'opsz' 48";
    icon.style.color = !isChecked ? color : "gray";
}

function switchBorderColor(id, color, isChecked) {
    const container = document.getElementById("container_" + id);
    container.style.borderColor = !isChecked ? color : "lightGray";
}

function updateLightSwitch(toggle, id) {
    const isChecked = toggle.getAttribute('aria-checked') === 'true';
    switchToggle(toggle, isChecked);
    switchIcon(id, "orange", isChecked);
    switchBorderColor(id, "orange", isChecked);
    ajaxUpdateValue(toggle.getAttribute('aria-checked'), id);
}

function updateValueLabel(value, id, measurementUnit = "") {
    const label = document.getElementById("valueLabel_" + id);
    label.innerHTML = value + measurementUnit;
}

function updateSlider(sliderValue, id) {
    updateValueLabel(sliderValue, id, "%");
    const isChecked = sliderValue === "0"
    switchIcon(id, "orange", isChecked);
    switchBorderColor(id, "orange", isChecked);
    const icon = document.getElementById("icon_" + id);
    if (isChecked)
        icon.innerHTML = "brightness_5"
    else if (sliderValue === "100")
        icon.innerHTML = "brightness_7"
    else
        icon.innerHTML = "brightness_6"
    ajaxUpdateValue(sliderValue, id);
}

function ajaxUpdateValue(value, id) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_device');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
            console.log('Value updated successfully.');
        } else {
            console.error('Value update failed.');
        }
    };
    const data = {value, id}
    xhr.send(JSON.stringify(data));
}