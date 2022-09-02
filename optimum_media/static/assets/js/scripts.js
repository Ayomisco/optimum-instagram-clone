
const fileInput = document.querySelector('#js-uploader input[type=file]');
fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
        const fileName = document.querySelector('#js-uploader .file-name');
        fileName.textContent = fileInput.files[0].name;
    }
}
