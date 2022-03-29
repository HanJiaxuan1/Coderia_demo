window.onload = function () {

const getEl = id => document.getElementById(id);

const iFrame = getEl('iFrame').contentWindow.document;
const htmlTextArea = getEl('htmlTextarea');
const cssTextArea = getEl('cssTextarea');
const jsTextArea = getEl('jsTextarea');

document.body.onkeyup = function () {
    iFrame.open();
    iFrame.writeln(
        htmlTextArea.value +
        '<style>' +
        cssTextArea.value +
        '</style>' +
        '<script>' +
        jsTextArea.value +
        '</script>'
    );
    iFrame.close();
};

};